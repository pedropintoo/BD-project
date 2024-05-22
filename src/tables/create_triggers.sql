--################################# Author #################################--
DROP TRIGGER IF EXISTS trg_author_ArticlesCount_Insert;
DROP TRIGGER IF EXISTS trg_author_ArticlesCount_Delete;
DROP TRIGGER IF EXISTS trg_author_ArticlesCount_Update;
--------------------------------------------------------------------------------

CREATE TRIGGER trg_author_ArticlesCount_Insert
ON Wrote_by AFTER INSERT AS
BEGIN
    UPDATE Author
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID)
    FROM Author
    INNER JOIN inserted i ON Author.AuthorID = i.AuthorID
END;

CREATE TRIGGER trg_author_ArticlesCount_Delete
ON Wrote_by AFTER DELETE AS
BEGIN
    UPDATE Author
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID)
    FROM Author
    INNER JOIN deleted d ON Author.AuthorID = d.AuthorID
END;

CREATE TRIGGER trg_author_ArticlesCount_Update
ON Wrote_by AFTER UPDATE AS
BEGIN
    -- Update previous ArticlesCount
    UPDATE Author
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID)
    FROM Author
    INNER JOIN deleted d ON Author.AuthorID = d.AuthorID

    -- Update current ArticlesCount
    UPDATE Author
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID) 
    FROM Author
    INNER JOIN inserted i ON Author.AuthorID = i.AuthorID
END;


--################################# Institution #################################--
DROP TRIGGER IF EXISTS trg_institution_AuthorsCount_Insert;
DROP TRIGGER IF EXISTS trg_institution_AuthorsCount_Delete;
DROP TRIGGER IF EXISTS trg_institution_AuthorsCount_Update;
--------------------------------------------------------------------------------

CREATE TRIGGER trg_institution_AuthorsCount_Insert
ON Author AFTER INSERT AS
BEGIN
    UPDATE Institution
    SET AuthorsCount = (SELECT COALESCE(COUNT(*), 0) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN inserted i ON Institution.InstitutionID = i.InstitutionID
END;

CREATE TRIGGER trg_institution_AuthorsCount_Delete
ON Author AFTER DELETE AS
BEGIN
    UPDATE Institution
    SET AuthorsCount = (SELECT COALESCE(COUNT(*), 0) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN deleted i ON Institution.InstitutionID = i.InstitutionID
END;

CREATE TRIGGER trg_institution_AuthorsCount_Update
ON Author AFTER UPDATE AS
BEGIN
    -- Update previous AuthorsCount
    UPDATE Institution
    SET AuthorsCount = (SELECT COALESCE(COUNT(*), 0) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN deleted d ON Institution.InstitutionID = d.InstitutionID

    -- Update current AuthorsCount
    UPDATE Institution
    SET AuthorsCount = (SELECT COALESCE(COUNT(*), 0) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN inserted i ON Institution.InstitutionID = i.InstitutionID
END;

--################################# Topic #################################--
DROP TRIGGER IF EXISTS trg_topic_ArticlesCount_Insert;
DROP TRIGGER IF EXISTS trg_topic_ArticlesCount_Delete;
DROP TRIGGER IF EXISTS trg_topic_ArticlesCount_Update;
--------------------------------------------------------------------------------

CREATE TRIGGER trg_topic_ArticlesCount_Insert
ON Belongs_to AFTER INSERT AS
BEGIN
    UPDATE Topic
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Belongs_to WHERE Belongs_to.TopicID = Topic.TopicID)
    FROM Topic
    INNER JOIN inserted i ON Topic.TopicID = i.TopicID
END;

CREATE TRIGGER trg_topic_ArticlesCount_Delete
ON Belongs_to AFTER DELETE AS
BEGIN
    UPDATE Topic
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Belongs_to WHERE Belongs_to.TopicID = Topic.TopicID)
    FROM Topic
    INNER JOIN deleted d ON Topic.TopicID = d.TopicID
END;

CREATE TRIGGER trg_topic_ArticlesCount_Update
ON Belongs_to AFTER UPDATE AS
BEGIN
    -- Update previous ArticlesCount
    UPDATE Topic
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Belongs_to WHERE Belongs_to.TopicID = Topic.TopicID)
    FROM Topic
    INNER JOIN deleted d ON Topic.TopicID = d.TopicID

    -- Update current ArticlesCount
    UPDATE Topic
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Belongs_to WHERE Belongs_to.TopicID = Topic.TopicID)
    FROM Topic
    INNER JOIN inserted i ON Topic.TopicID = i.TopicID
END;

--################################# Journal #################################--
DROP TRIGGER IF EXISTS trg_UpdateArticlesCountJournal_Insert;
DROP TRIGGER IF EXISTS trg_UpdateArticlesCountJournal_Delete;
DROP TRIGGER IF EXISTS trg_UpdateArticlesCountJournal_Update;
--------------------------------------------------------------------------------

CREATE TRIGGER trg_UpdateArticlesCountJournal_Insert
ON Article AFTER INSERT AS
BEGIN
    UPDATE Journal
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Article WHERE Article.JournalID = Journal.JournalID)
    FROM Journal
    INNER JOIN inserted i ON Journal.JournalID = i.JournalID
END;

CREATE TRIGGER trg_UpdateArticlesCountJournal_Delete
ON Article AFTER DELETE AS
BEGIN
    UPDATE Journal
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Article WHERE Article.JournalID = Journal.JournalID)
    FROM Journal
    INNER JOIN deleted d ON Journal.JournalID = d.JournalID
END;

CREATE TRIGGER trg_UpdateArticlesCountJournal_Update
ON Article AFTER UPDATE AS
BEGIN
    -- Update previous ArticlesCount
    UPDATE Journal
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Article WHERE Article.JournalID = Journal.JournalID)
    FROM Journal
    INNER JOIN deleted d ON Journal.JournalID = d.JournalID

    -- Update current ArticlesCount
    UPDATE Journal
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Article WHERE Article.JournalID = Journal.JournalID)
    FROM Journal
    INNER JOIN inserted i ON Journal.JournalID = i.JournalID
END;

