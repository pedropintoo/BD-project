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
-- CREATE NONCLUSTERED INDEX IDX_Institution_Name
-- ON Institution ([Name]);

-- CREATE NONCLUSTERED INDEX IDX_Institution_AuthorsCount
-- ON Institution (AuthorsCount);

