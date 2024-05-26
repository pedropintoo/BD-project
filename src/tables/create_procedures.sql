--################################# Chart #################################--
DROP PROCEDURE IF EXISTS Top3TopicsPerYear;
DROP PROCEDURE IF EXISTS MostProductiveAuthorsByTopic;
DROP PROCEDURE IF EXISTS RunningCitationsSumPerTopic;
--------------------------------------------------------------------------------

CREATE PROCEDURE Top3TopicsPerYear
AS
BEGIN
    SELECT PublicationYear, T.TopicName, TopicCount
    FROM (
        SELECT COUNT(L.TopicID) AS TopicCount, L.TopicName AS TopicName, RANK() OVER (PARTITION BY YEAR(PublicationDate) ORDER BY COUNT(L.TopicID) DESC, L.TopicName) AS rank_pub, YEAR(PublicationDate) AS PublicationYear
        FROM ListAllArticlesPerTopic() AS L
        INNER JOIN JournalVolume ON JournalVolume.JournalID = L.JournalID 
        GROUP BY L.TopicName, YEAR(PublicationDate)
    ) AS T
    WHERE T.rank_pub <= 3
    ORDER BY T.PublicationYear DESC, T.rank_pub
END;


CREATE PROCEDURE MostProductiveAuthorsByTopic
AS
BEGIN
    SELECT TOP 8 TopicName, AuthorName, ArticlesCount
    FROM (
        SELECT COUNT(Author.ArticlesCount) AS ArticlesCount, ROW_NUMBER() OVER (PARTITION BY TopicName ORDER BY COUNT(Author.ArticlesCount) DESC, L.TopicName) AS AuthorRank, Author.AuthorID, Author.[Name] AS AuthorName, L.TopicName
        FROM ListAllArticlesPerTopic() AS L
        INNER JOIN Wrote_by ON Wrote_by.ArticleID = L.ArticleID
        INNER JOIN Author ON Author.AuthorID = Wrote_by.AuthorID
        GROUP BY Author.AuthorID, Author.[Name], L.TopicName
    ) AS T
    WHERE T.AuthorRank = 1
    ORDER BY T.ArticlesCount DESC
END;

CREATE PROCEDURE RunningCitationsSumPerTopic
AS
BEGIN
    SET NOCOUNT ON

    DECLARE @TopicName		VARCHAR(50)
    DECLARE @CitationsCount INT
    DECLARE @RunningSum		INT = 0

    -- Create a temporary table to store the results
    CREATE TABLE #CitationsSummary (
        TopicName		VARCHAR(50),
        CitationsCount          INT,
        RunningCitationsSum		INT
    )

    DECLARE runningSumCursor CURSOR FAST_FORWARD
    FOR 
        -- Citations per topic
        SELECT TopicName, COUNT(TopicID) AS CitationsCount
        FROM ListAllArticlesPerTopic() AS L
        INNER JOIN Cited_by ON CitedArticleID = ArticleID
        GROUP BY TopicName
        ORDER BY CitationsCount

    OPEN runningSumCursor

    FETCH NEXT FROM runningSumCursor INTO @TopicName, @CitationsCount
    

    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Add the current CitationsCount to the running sum
        SET @RunningSum = @RunningSum + @CitationsCount

        -- Insert the current row's data and the running sum into the temporary table
        INSERT INTO #CitationsSummary (TopicName, CitationsCount, RunningCitationsSum)
        VALUES (@TopicName, @CitationsCount, @RunningSum)

        -- Fetch the next row from the cursor
        FETCH NEXT FROM runningSumCursor INTO @TopicName, @CitationsCount
    END

    -- end the cursor
    CLOSE runningSumCursor
    DEALLOCATE runningSumCursor

    -- Return the result
    SELECT * FROM #CitationsSummary
    DROP TABLE #CitationsSummary
END;


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
    WHERE [Name] LIKE '%' + @AuthorName + '%'
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
    WHERE [Name] LIKE '%' + @InstitutionName + '%'
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
    WHERE [Name] LIKE '%' + @TopicName + '%'
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
    WHERE [Name] LIKE '%' + @JournalName + '%'
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


--################################# Article #################################--
-- listing
DROP PROCEDURE IF EXISTS OrderByArticleTitle;
DROP PROCEDURE IF EXISTS OrderBySearchArticleTitle;
DROP PROCEDURE IF EXISTS OrderByAuthorsCount_article; -- slightly different name
-- details
DROP PROCEDURE IF EXISTS ListArticleDetails;
DROP PROCEDURE IF EXISTS GetJournalIDByName;
-- delete/update/create
DROP PROCEDURE IF EXISTS DeleteArticle;
DROP PROCEDURE IF EXISTS ValidateArticle;
DROP PROCEDURE IF EXISTS UpdateArticle;
DROP PROCEDURE IF EXISTS CreateArticle;
--------------------------------------------------------------------------------

-- listing
CREATE PROCEDURE OrderByArticleTitle
AS
BEGIN
    SELECT * 
    FROM ListAllArticles()
    ORDER BY Title
END;

CREATE PROCEDURE OrderByAuthorsCount_article
AS
BEGIN
    SELECT * 
    FROM ListAllArticles()
    ORDER BY AuthorsCount DESC
END;

CREATE PROCEDURE OrderBySearchArticleTitle (@ArticleTitle NVARCHAR(500))
AS
BEGIN
    SELECT * FROM ListAllArticles() 
    WHERE Title LIKE '%' + @ArticleTitle + '%'
    ORDER BY Title
END;

-- details
CREATE PROCEDURE ListArticleDetails
    @ArticleID VARCHAR(10)
AS
BEGIN
    SELECT 
        Article.Title, 
        Article.Abstract, 
        Article.DOI, 
        Article.StartPage, 
        Article.EndPage, 
        Journal.[Name] AS JournalName, 
        JournalVolume.Volume, 
        JournalVolume.PublicationDate, 
        Article.AuthorsCount
    FROM Article
    LEFT JOIN JournalVolume ON JournalVolume.JournalID = Article.JournalID AND JournalVolume.Volume = Article.Volume
    LEFT JOIN Journal ON Journal.JournalID = Article.JournalID
    WHERE Article.ArticleID = @ArticleID

    -- list of authors
    SELECT Author.Name
    FROM Author
    INNER JOIN (
        SELECT AuthorID
        FROM Wrote_by
        WHERE ArticleID = @ArticleID
    ) AS ArticleAuthors ON Author.AuthorID = ArticleAuthors.AuthorID

    -- list of topics
    SELECT Topic.Name
    FROM Topic
    INNER JOIN (
        SELECT TopicID
        FROM Belongs_to
        WHERE ArticleID = @ArticleID
    ) AS ArticleTopics ON Topic.TopicID = ArticleTopics.TopicID

END;


CREATE PROCEDURE GetJournalIDByName
    @JournalName VARCHAR(100),
    @JournalID VARCHAR(40) OUTPUT
AS
BEGIN
    SELECT @JournalID = JournalID
    FROM Journal
    WHERE [Name] = @JournalName
END;

-- delete/update/create
CREATE PROCEDURE DeleteArticle
    @ArticleID VARCHAR(10)
AS
BEGIN
    SET NOCOUNT ON

    -- start transaction
    BEGIN TRANSACTION

    BEGIN TRY
        -- Remove related records in the Wrote_by table
        DELETE FROM Wrote_by
        WHERE ArticleID = @ArticleID

        -- Remove related records in the Belongs_to table
        DELETE FROM Belongs_to
        WHERE ArticleID = @ArticleID

        -- Remove related records in the Cited_by table
        DELETE FROM Cited_by
        WHERE CitedArticleID = @ArticleID OR CitingArticleID = @ArticleID

        -- Remove related records in the Has_Keywords table
        DELETE FROM Has_Keywords
        WHERE ArticleID = @ArticleID

        -- Remove related records in the Favorite_Article table
        DELETE FROM Favorite_Article
        WHERE ArticleID = @ArticleID

        -- Remove related records in the Read_by table
        DELETE FROM Read_by
        WHERE ArticleID = @ArticleID

        -- Remove the article
        DELETE FROM Article
        WHERE ArticleID = @ArticleID

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

CREATE PROCEDURE ValidateArticle
    @Title NVARCHAR(500),
    @JournalName VARCHAR(100),
    @Volume INT,
    @StartPage INT,
    @EndPage INT,
    @JourID VARCHAR(40) OUTPUT
AS
BEGIN 
    IF @Title IS NULL
    BEGIN
        RAISERROR ('Article title cannot be empty.', 16, 1)
        RETURN
    END

    EXEC GetJournalIDByName @JournalName, @JournalID = @JourID OUTPUT

    -- Check if JournalID is NULL and JournalName is not empty
    IF @JourID is NULL AND @JournalName IS NOT NULL
    BEGIN
        RAISERROR ('Journal %s not found.', 16, 1, @JournalName)
        RETURN
    END

    -- Check if Volume is NULL and JournalName is not empty
    IF @Volume is NULL AND @JournalName IS NOT NULL
    BEGIN
        RAISERROR ('Volume cannot be empty.', 16, 1)
        RETURN
    END

    -- Check if Volume is valid
    IF @JournalName IS NOT NULL AND NOT EXISTS (SELECT 1 FROM JournalVolume WHERE JournalID = @JourID AND Volume = @Volume)
    BEGIN
        RAISERROR ('Volume %d not found for journal %s.', 16, 1, @Volume, @JournalName)
        RETURN
    END

    -- Check if StartPage is bigger than EndPage
    IF @StartPage IS NOT NULL AND @EndPage IS NOT NULL AND @StartPage > @EndPage
    BEGIN
        RAISERROR ('Start page cannot be bigger than end page.', 16, 1)
        RETURN
    END
    

END;


CREATE PROCEDURE UpdateArticle
    @ArticleID VARCHAR(10),
    @Title NVARCHAR(500),
    @Abstract VARCHAR(1250),
    @DOI VARCHAR(50),
    @StartPage INT,
    @EndPage INT,
    @JournalName VARCHAR(100),
    @Volume INT
AS
BEGIN
    SET NOCOUNT ON

    -- normalize the args
    SET @Title = NULLIF(@Title, '')
    SET @Abstract = NULLIF(@Abstract, '')
    SET @DOI = NULLIF(@DOI, '')
    SET @StartPage = NULLIF(@StartPage, 0)
    SET @EndPage = NULLIF(@EndPage, 0)
    SET @JournalName = NULLIF(@JournalName, '')
    SET @Volume = NULLIF(@Volume, 0)

    DECLARE @JourID VARCHAR(40)
    EXEC ValidateArticle @Title, @JournalName, @Volume, @StartPage, @EndPage, @JourID OUTPUT -- exception may be thrown

    UPDATE Article
    SET Title = @Title, Abstract = @Abstract, DOI = @DOI, StartPage = @StartPage, EndPage = @EndPage, JournalID = @JourID, Volume = @Volume
    WHERE ArticleID = @ArticleID
END;    

CREATE PROCEDURE CreateArticle
    @ArticleID VARCHAR(10),
    @Title NVARCHAR(500),
    @Abstract VARCHAR(1250),
    @DOI VARCHAR(50),
    @StartPage INT,
    @EndPage INT,
    @JournalName VARCHAR(100),
    @Volume INT
AS
BEGIN    
    SET NOCOUNT ON

    -- normalize the args
    SET @Title = NULLIF(@Title, '')
    SET @Abstract = NULLIF(@Abstract, '')
    SET @DOI = NULLIF(@DOI, '')
    SET @StartPage = NULLIF(@StartPage, 0)
    SET @EndPage = NULLIF(@EndPage, 0)
    SET @JournalName = NULLIF(@JournalName, '')
    SET @Volume = NULLIF(@Volume, 0)

    DECLARE @JourID VARCHAR(40)
    EXEC ValidateArticle @Title, @JournalName, @Volume, @StartPage, @EndPage, @JourID OUTPUT -- exception may be thrown

    INSERT INTO Article (ArticleID, Title, Abstract, DOI, StartPage, EndPage, JournalID, Volume, AuthorsCount) 
    VALUES (@ArticleID, @Title, @Abstract, @DOI, @StartPage, @EndPage, @JourID, @Volume, 0)
END;