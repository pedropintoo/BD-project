--################################# Author #################################--
-- listing
DROP PROCEDURE IF EXISTS OrderByAuthorName;
DROP PROCEDURE IF EXISTS OrderBySearchAuthorName;
DROP PROCEDURE IF EXISTS OrderByArticlesCount;  
-- details
DROP PROCEDURE IF EXISTS ListAuthorDetails;
DROP PROCEDURE IF EXISTS GetInstitutionIDByName;
-- delete/update/create
DROP PROCEDURE IF EXISTS DeleteAuthor;
DROP PROCEDURE IF EXISTS ValidateAuthorName;
DROP PROCEDURE IF EXISTS UpdateAuthor;
DROP PROCEDURE IF EXISTS CreateAuthor;
--------------------------------------------------------------------------------

-- listing
CREATE PROCEDURE OrderByAuthorName 
AS
BEGIN
    SELECT * 
    FROM ListAllAuthors()
    ORDER BY [Name]
END;

CREATE PROCEDURE OrderByArticlesCount 
AS
BEGIN
    SELECT * 
    FROM ListAllAuthors()
    ORDER BY ArticlesCount DESC
END;    

CREATE PROCEDURE OrderBySearchAuthorName (@AuthorName NVARCHAR(50))
AS
BEGIN
    SELECT * FROM ListAllAuthors() 
    WHERE [Name] LIKE @AuthorName + '%'
    ORDER BY [Name]
END;

-- details
CREATE PROCEDURE ListAuthorDetails
    @AuthorID VARCHAR(10)
AS
BEGIN
    SELECT 
        Author.Name, 
        Author.[Url], 
        Author.ORCID, 
        Institution.Name AS InstitutionName,
        Author.ArticlesCount
    FROM Author
    LEFT JOIN Institution ON Institution.InstitutionID = Author.InstitutionID
    WHERE Author.AuthorID = @AuthorID

    -- list of articles
    SELECT Article.Title
    FROM Article
    INNER JOIN (
        SELECT ArticleID
        FROM Wrote_by
        WHERE AuthorID = @AuthorID
    ) AS AuthorArticles ON Article.ArticleID = AuthorArticles.ArticleID

END;

CREATE PROCEDURE GetInstitutionIDByName
    @InstitutionName VARCHAR(300),
    @InstitutionID VARCHAR(10) OUTPUT
AS
BEGIN
    SELECT @InstitutionID = InstitutionID
    FROM Institution
    WHERE [Name] = @InstitutionName
END;

-- delete/update/create
CREATE PROCEDURE DeleteAuthor
    @AuthorID VARCHAR(10)
AS
BEGIN
    SET NOCOUNT ON

    -- Start a transaction
    BEGIN TRANSACTION

    BEGIN TRY
        -- Remove related records in the Wrote_by table
        DELETE FROM Wrote_by
        WHERE AuthorID = @AuthorID

        -- Remove the author
        DELETE FROM Author
        WHERE AuthorID = @AuthorID

        -- Commit the transaction
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        -- Rollback the transaction in case of an error
        ROLLBACK TRANSACTION

        -- Rethrow the error
        THROW
    END CATCH
END;

CREATE PROCEDURE ValidateAuthorName
    @Name NVARCHAR(50),
    @InstitutionName VARCHAR(300),
    @InstID VARCHAR(10) OUTPUT
AS
BEGIN
    IF @Name IS NULL
    BEGIN
        RAISERROR ('Author name cannot be empty.', 16, 1)
        RETURN
    END

    EXEC GetInstitutionIDByName @InstitutionName, @InstitutionID = @InstID OUTPUT

    -- Check if InstitutionID is NULL and InstitutionName is not empty
    IF @InstID is NULL AND @InstitutionName IS NOT NULL
    BEGIN
        RAISERROR ('Institution %s not found.', 16, 1, @InstitutionName)
        RETURN
    END
END;

CREATE PROCEDURE UpdateAuthor
    @AuthorID VARCHAR(10),
    @Name NVARCHAR(50),
    @Url VARCHAR(100),
    @ORCID VARCHAR(19),
    @InstitutionName VARCHAR(300)
AS
BEGIN
    SET NOCOUNT ON

    -- normalize the args
    SET @Name = NULLIF(@Name, '')
    SET @Url = NULLIF(@Url, '')
    SET @ORCID = NULLIF(@ORCID, '')
    SET @InstitutionName = NULLIF(@InstitutionName, '')

    DECLARE @InstID VARCHAR(10)
    EXEC ValidateAuthorName @Name, @InstitutionName, @InstID OUTPUT -- exception may be thrown

    UPDATE Author
    SET [Name] = @Name, [Url] = @Url, ORCID = @ORCID, InstitutionID = @InstID
    WHERE AuthorID = @AuthorID
    
END;

CREATE PROCEDURE CreateAuthor
    @AuthorID VARCHAR(10),
    @Name NVARCHAR(50),
    @Url VARCHAR(100),
    @ORCID VARCHAR(19),
    @InstitutionName VARCHAR(300)
AS
BEGIN
    SET NOCOUNT ON

    -- normalize the args
    SET @Name = NULLIF(@Name, '')
    SET @Url = NULLIF(@Url, '')
    SET @ORCID = NULLIF(@ORCID, '')
    SET @InstitutionName = NULLIF(@InstitutionName, '')

    DECLARE @InstID VARCHAR(10)
    EXEC ValidateAuthorName @Name, @InstitutionName, @InstID OUTPUT -- exception may be thrown

    INSERT INTO Author (AuthorID, [Name], [Url], ORCID, InstitutionID, ArticlesCount) 
    VALUES (@AuthorID, @Name, @Url, @ORCID, @InstID, 0)
END;



--################################# Institution #################################--
-- listing
DROP PROCEDURE IF EXISTS OrderByInstitutionName;
DROP PROCEDURE IF EXISTS OrderBySearchInstitutionName;
DROP PROCEDURE IF EXISTS OrderByAuthorsCount;
-- details
DROP PROCEDURE IF EXISTS ListInstitutionDetails;
-- delete/update/create
DROP PROCEDURE IF EXISTS DeleteInstitution;
DROP PROCEDURE IF EXISTS ValidateInstitutionName;
DROP PROCEDURE IF EXISTS UpdateInstitution;
DROP PROCEDURE IF EXISTS CreateInstitution;
--------------------------------------------------------------------------------

-- listing
CREATE PROCEDURE OrderByInstitutionName 
AS
BEGIN
    SELECT * 
    FROM ListAllInstitutions()
    ORDER BY [Name]
END;

CREATE PROCEDURE OrderByAuthorsCount 
AS
BEGIN
    SELECT * 
    FROM ListAllInstitutions()
    ORDER BY AuthorsCount DESC
END;    

CREATE PROCEDURE OrderBySearchInstitutionName (@InstitutionName NVARCHAR(50))
AS 
BEGIN
    SELECT * FROM ListAllInstitutions() 
    WHERE [Name] LIKE @InstitutionName + '%'
    ORDER BY [Name]
END;

-- details
CREATE PROCEDURE ListInstitutionDetails
    @InstitutionID VARCHAR(10)
AS
BEGIN
    SELECT 
        Institution.Name, 
        Institution.Address,
        Institution.AuthorsCount
    FROM Institution
    WHERE Institution.InstitutionID = @InstitutionID

    -- list of authors
    SELECT Author.Name 
    FROM Author
    WHERE Author.InstitutionID = @InstitutionID
END;

-- delete/update/create
CREATE PROCEDURE DeleteInstitution
    @InstitutionID VARCHAR(10)
AS
BEGIN
    SET NOCOUNT ON

    -- start transaction
    BEGIN TRANSACTION

    BEGIN TRY
        -- Set InstitutionID to NULL in other tables
        UPDATE Author
        SET InstitutionID = NULL
        WHERE InstitutionID = @InstitutionID

        UPDATE [User]
        SET InstitutionID = NULL
        WHERE InstitutionID = @InstitutionID

        -- Delete the institution
        DELETE FROM Institution
        WHERE InstitutionID = @InstitutionID

        -- Commit the transaction
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        -- Rollback the transaction in case of an error
        ROLLBACK TRANSACTION

        -- Rethrow the error
        THROW
    END CATCH
END;

CREATE PROCEDURE ValidateInstitutionName
    @Name NVARCHAR(50)
AS
BEGIN
    IF @Name IS NULL
    BEGIN
        RAISERROR ('Institution name cannot be empty.', 16, 1)
        RETURN
    END
END;

CREATE PROCEDURE UpdateInstitution
    @InstitutionID VARCHAR(10),
    @Name NVARCHAR(50),
    @Address VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON

    -- normalize the args
    SET @Name = NULLIF(@Name, '')
    SET @Address = NULLIF(@Address, '')

    EXEC ValidateInstitutionName @Name -- exception may be thrown

    UPDATE Institution
    SET [Name] = @Name, [Address] = @Address
    WHERE InstitutionID = @InstitutionID
END;

CREATE PROCEDURE CreateInstitution
    @InstitutionID VARCHAR(10),
    @Name NVARCHAR(50),
    @Address VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON

    -- normalize the args
    SET @Name = NULLIF(@Name, '')
    SET @Address = NULLIF(@Address, '')

    EXEC ValidateInstitutionName @Name -- exception may be thrown

    INSERT INTO Institution (InstitutionID, [Name], [Address], AuthorsCount) 
    VALUES (@InstitutionID, @Name, @Address, 0)
END;


--################################# Topic #################################--
-- listing
DROP PROCEDURE IF EXISTS OrderByTopicName;
DROP PROCEDURE IF EXISTS OrderBySearchTopicName;
DROP PROCEDURE IF EXISTS OrderByArticlesCount_topic; -- slightly different name
-- details
DROP PROCEDURE IF EXISTS ListTopicDetails;
-- delete/update/create
DROP PROCEDURE IF EXISTS DeleteTopic;
DROP PROCEDURE IF EXISTS ValidateTopicName;
DROP PROCEDURE IF EXISTS UpdateTopic;
DROP PROCEDURE IF EXISTS CreateTopic;
--------------------------------------------------------------------------------

-- listing
CREATE PROCEDURE OrderByTopicName
AS
BEGIN
    SELECT * 
    FROM ListAllTopics()
    ORDER BY [Name]
END;

CREATE PROCEDURE OrderByArticlesCount_topic
AS
BEGIN
    SELECT * 
    FROM ListAllTopics()
    ORDER BY ArticlesCount DESC
END;

CREATE PROCEDURE OrderBySearchTopicName (@TopicName NVARCHAR(50))
AS
BEGIN
    SELECT * FROM ListAllTopics() 
    WHERE [Name] LIKE @TopicName + '%'
    ORDER BY [Name]
END;

-- details
CREATE PROCEDURE ListTopicDetails
    @TopicID VARCHAR(10)
AS
BEGIN

    -- Count users who are interested in this topic
    SELECT COALESCE(COUNT(*), 0) FROM Interested_in WHERE TopicID = @TopicID

    SELECT 
        Topic.Name, 
        Topic.Description,
        Topic.ArticlesCount
    FROM Topic
    WHERE Topic.TopicID = @TopicID

    -- list of articles
    SELECT Article.Title
    FROM Article
    INNER JOIN (
        SELECT ArticleID
        FROM Belongs_to
        WHERE TopicID = @TopicID
    ) AS TopicArticles ON Article.ArticleID = TopicArticles.ArticleID

END;

-- delete/update/create
CREATE PROCEDURE DeleteTopic
    @TopicID VARCHAR(10)
AS
BEGIN
    SET NOCOUNT ON

    -- start transaction
    BEGIN TRANSACTION

    BEGIN TRY
        -- Remove related records
        DELETE FROM Interested_in
        WHERE TopicID = @TopicID

        DELETE FROM Belongs_to
        WHERE TopicID = @TopicID

        -- Delete the topic
        DELETE FROM Topic
        WHERE TopicID = @TopicID
        -- Commit the transaction
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        -- Rollback the transaction in case of an error
        ROLLBACK TRANSACTION

        -- Rethrow the error
        THROW
    END CATCH
END;

CREATE PROCEDURE ValidateTopicName
    @Name NVARCHAR(50)
AS
BEGIN
    IF @Name IS NULL
    BEGIN
        RAISERROR ('Topic name cannot be empty.', 16, 1)
        RETURN
    END
END;

CREATE PROCEDURE UpdateTopic
    @TopicID VARCHAR(10),
    @Name NVARCHAR(50),
    @Description NVARCHAR(300)
AS
BEGIN
    SET NOCOUNT ON

    -- normalize the args
    SET @Name = NULLIF(@Name, '')
        SET @Description = NULLIF(@Description, '')

    EXEC ValidateTopicName @Name -- exception may be thrown

    UPDATE Topic
    SET [Name] = @Name, [Description] = @Description
    WHERE TopicID = @TopicID
END;

CREATE PROCEDURE CreateTopic
    @TopicID VARCHAR(10),
    @Name NVARCHAR(50),
    @Description NVARCHAR(300)
AS
BEGIN
    SET NOCOUNT ON

    -- normalize the args
    SET @Name = NULLIF(@Name, '')
    SET @Description = NULLIF(@Description, '')

    EXEC ValidateTopicName @Name -- exception may be thrown

    INSERT INTO Topic (TopicID, [Name], [Description], ArticlesCount) 
    VALUES (@TopicID, @Name, @Description, 0)
END;


--################################# Journal #################################--
-- listing
DROP PROCEDURE IF EXISTS OrderByJournalName;
DROP PROCEDURE IF EXISTS OrderBySearchJournalName;
DROP PROCEDURE IF EXISTS OrderByArticlesCount_journal; -- slightly different name
-- details
DROP PROCEDURE IF EXISTS ListJournalDetails;
DROP PROCEDURE IF EXISTS GetJournalIDByName;
-- delete/update/create
DROP PROCEDURE IF EXISTS DeleteJournal;
DROP PROCEDURE IF EXISTS ValidateJournalName;
DROP PROCEDURE IF EXISTS UpdateJournal;
DROP PROCEDURE IF EXISTS CreateJournal;
--------------------------------------------------------------------------------

-- listing
CREATE PROCEDURE OrderByJournalName
AS
BEGIN
    SELECT * 
    FROM ListAllJournals()
    ORDER BY [Name]
END;

CREATE PROCEDURE OrderByArticlesCount_journal
AS
BEGIN
    SELECT * 
    FROM ListAllJournals()
    ORDER BY ArticlesCount DESC
END;

CREATE PROCEDURE OrderBySearchJournalName (@JournalName NVARCHAR(100))
AS
BEGIN
    SELECT * FROM ListAllJournals() 
    WHERE [Name] LIKE @JournalName + '%'
    ORDER BY [Name]
END;

CREATE PROCEDURE ListJournalDetails
    @JournalID VARCHAR(40)
AS
BEGIN
    -- Count users who are interested in this topic
    SELECT COALESCE(COUNT(*), 0) FROM Favorite_Journal WHERE JournalID = @JournalID

    SELECT 
        Journal.[Name], 
        Journal.PrintISSN, 
        Journal.EletronicISSN, 
        Journal.[Url], 
        Journal.Publisher, 
        Journal.ArticlesCount
    FROM Journal
    WHERE Journal.JournalID = @JournalID

    -- list of articles per volume   
    SELECT JournalVolume.JournalID, JournalVolume.Volume, JournalVolume.PublicationDate, Title
    FROM JournalVolume
    INNER JOIN (
        SELECT JournalID, Volume, Title
        FROM Article
        WHERE Article.JournalID = @JournalID
    ) AS JournalArticles ON JournalVolume.JournalID = JournalArticles.JournalID AND JournalVolume.Volume = JournalArticles.Volume
    ORDER BY JournalVolume.PublicationDate DESC

END;

-- delete/update/create
CREATE PROCEDURE DeleteJournal
    @JournalID VARCHAR(40)
AS
BEGIN
    SET NOCOUNT ON

    -- start transaction
    BEGIN TRANSACTION

    BEGIN TRY
        -- Update related records in the Article table
        UPDATE Article
        SET JournalID = NULL, Volume = NULL
        WHERE JournalID = @JournalID

        -- Remove related records in the JournalVolume table
        DELETE FROM JournalVolume
        WHERE JournalID = @JournalID

        -- Remove related records in the Favorite_Journal table
        DELETE FROM Favorite_Journal
        WHERE JournalID = @JournalID
 
        -- Remove the journal
        DELETE FROM Journal
        WHERE JournalID = @JournalID

        -- Commit the transaction
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        -- Rollback the transaction in case of an error
        ROLLBACK TRANSACTION

        -- Rethrow the error
        THROW
    END CATCH
END;

CREATE PROCEDURE ValidateJournalName
    @Name NVARCHAR(100)
AS
BEGIN
    IF @Name IS NULL
    BEGIN
        RAISERROR ('Journal name cannot be empty.', 16, 1)
        RETURN
    END
END;


CREATE PROCEDURE UpdateJournal
    @JournalID VARCHAR(40),
    @Name NVARCHAR(100),
    @PrintISSN VARCHAR(9),
    @EletronicISSN VARCHAR(9),
    @Url VARCHAR(100),
    @Publisher VARCHAR(50)
AS
BEGIN 
    SET NOCOUNT ON

    -- normalize the args
    SET @Name = NULLIF(@Name, '')
    SET @PrintISSN = NULLIF(@PrintISSN, '')
    SET @EletronicISSN = NULLIF(@EletronicISSN, '')
    SET @Url = NULLIF(@Url, '')
    SET @Publisher = NULLIF(@Publisher, '')

    EXEC ValidateJournalName @Name -- exception may be thrown

    UPDATE Journal
    SET [Name] = @Name, PrintISSN = @PrintISSN, EletronicISSN = @EletronicISSN, [Url] = @Url, Publisher = @Publisher
    WHERE JournalID = @JournalID

END;


CREATE PROCEDURE CreateJournal
    @JournalID VARCHAR(40),
    @Name NVARCHAR(100),
    @PrintISSN VARCHAR(9),
    @EletronicISSN VARCHAR(9),
    @Url VARCHAR(100),
    @Publisher VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON

    -- normalize the args
    SET @Name = NULLIF(@Name, '')
    SET @PrintISSN = NULLIF(@PrintISSN, '')
    SET @EletronicISSN = NULLIF(@EletronicISSN, '')
    SET @Url = NULLIF(@Url, '')
    SET @Publisher = NULLIF(@Publisher, '')

    EXEC ValidateJournalName @Name -- exception may be thrown

    INSERT INTO Journal (JournalID, [Name], PrintISSN, EletronicISSN, [Url], Publisher, ArticlesCount)
    VALUES (@JournalID, @Name, @PrintISSN, @EletronicISSN, @Url, @Publisher, 0)
END;        





