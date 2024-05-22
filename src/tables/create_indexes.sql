--################################# Author #################################--
-- indexes
IF IndexProperty(Object_ID('Author'), 'IDX_Author_Name', 'IndexId') IS NOT NULL
    DROP INDEX IDX_Author_Name ON Author;
IF IndexProperty(Object_ID('Author'), 'IDX_Author_ArticlesCount', 'IndexId') IS NOT NULL
    DROP INDEX IDX_Author_ArticlesCount ON Author;
-----------------------------------------------------------------------------

-- indexes
CREATE NONCLUSTERED INDEX IDX_Author_Name
ON Author ([Name]);

CREATE NONCLUSTERED INDEX IDX_Author_ArticlesCount
ON Author (ArticlesCount);

--################################# Institution #################################--
-- indexes
IF IndexProperty(Object_ID('Institution'), 'IDX_Institution_Name', 'IndexId') IS NOT NULL 
    DROP INDEX IDX_Institution_Name ON Institution;
IF IndexProperty(Object_ID('Institution'), 'IDX_Institution_AuthorsCount', 'IndexId') IS NOT NULL
    DROP INDEX IDX_Institution_AuthorsCount ON Institution;
-----------------------------------------------------------------------------

-- indexes
CREATE NONCLUSTERED INDEX IDX_Institution_Name
ON Institution ([Name]);

CREATE NONCLUSTERED INDEX IDX_Institution_AuthorsCount
ON Institution (AuthorsCount);

--################################# Topic #################################--
-- indexes
IF IndexProperty(Object_ID('Topic'), 'IDX_Topic_Name', 'IndexId') IS NOT NULL
    DROP INDEX IDX_Topic_Name ON Topic;
IF IndexProperty(Object_ID('Topic'), 'IDX_Topic_ArticlesCount', 'IndexId') IS NOT NULL
    DROP INDEX IDX_Topic_ArticlesCount ON Topic;
-----------------------------------------------------------------------------

-- indexes
CREATE NONCLUSTERED INDEX IDX_Topic_Name
ON Topic ([Name]);

CREATE NONCLUSTERED INDEX IDX_Topic_ArticlesCount
ON Topic (ArticlesCount);

--################################# Journal #################################--
-- indexes
IF IndexProperty(Object_ID('Journal'), 'IDX_Journal_Name', 'IndexId') IS NOT NULL
    DROP INDEX IDX_Journal_Name ON Journal;
IF IndexProperty(Object_ID('Journal'), 'IDX_Journal_ArticlesCount', 'IndexId') IS NOT NULL    
    DROP INDEX IDX_Journal_ArticlesCount ON Journal;
-----------------------------------------------------------------------------    

-- indexes
CREATE NONCLUSTERED INDEX IDX_Journal_Name
ON Journal ([Name]);

CREATE NONCLUSTERED INDEX IDX_Journal_ArticlesCount
ON Journal (ArticlesCount);