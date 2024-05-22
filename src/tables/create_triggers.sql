--################################# Author #################################--
DROP TRIGGER IF EXISTS trg_UpdateArticlesCount_Insert;
DROP TRIGGER IF EXISTS trg_UpdateArticlesCount_Delete;
DROP TRIGGER IF EXISTS trg_UpdateArticlesCount_Update;
--------------------------------------------------------------------------------

CREATE TRIGGER trg_UpdateArticlesCount_Insert
ON Wrote_by AFTER INSERT AS
BEGIN
    UPDATE Author
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID)
    FROM Author
    INNER JOIN inserted i ON Author.AuthorID = i.AuthorID
END;

CREATE TRIGGER trg_UpdateArticlesCount_Delete
ON Wrote_by AFTER DELETE AS
BEGIN
    UPDATE Author
    SET ArticlesCount = (SELECT COALESCE(COUNT(*), 0) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID)
    FROM Author
    INNER JOIN deleted d ON Author.AuthorID = d.AuthorID
END;

CREATE TRIGGER trg_UpdateArticlesCount_Update
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
DROP TRIGGER IF EXISTS trg_UpdateAuthorsCount_Insert;
DROP TRIGGER IF EXISTS trg_UpdateAuthorsCount_Delete;
DROP TRIGGER IF EXISTS trg_UpdateAuthorsCount_Update;
--------------------------------------------------------------------------------

CREATE TRIGGER trg_UpdateAuthorsCount_Insert
ON Author AFTER INSERT AS
BEGIN
    UPDATE Institution
    SET AuthorsCount = (SELECT COALESCE(COUNT(*), 0) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN inserted i ON Institution.InstitutionID = i.InstitutionID
END;

CREATE TRIGGER trg_UpdateAuthorsCount_Delete
ON Author AFTER DELETE AS
BEGIN
    UPDATE Institution
    SET AuthorsCount = (SELECT COALESCE(COUNT(*), 0) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN deleted i ON Institution.InstitutionID = i.InstitutionID
END;

CREATE TRIGGER trg_UpdateAuthorsCount_Update
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

