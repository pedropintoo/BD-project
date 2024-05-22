--################################# Author #################################--
DROP FUNCTION IF EXISTS ListAllAuthors;
------------------------------------------------------------------------------

CREATE FUNCTION ListAllAuthors()
RETURNS TABLE AS
RETURN
(
    SELECT 
        Author.AuthorID, 
        Author.Name, 
        Author.[Url], 
        Institution.Name AS InstitutionName,
        Author.ArticlesCount
    FROM Author 
    LEFT JOIN Institution ON Institution.InstitutionID = Author.InstitutionID
);


--################################# Institution #################################--
DROP FUNCTION IF EXISTS ListAllInstitutions;
------------------------------------------------------------------------------

CREATE FUNCTION ListAllInstitutions()
RETURNS TABLE AS
RETURN
(
    SELECT 
        Institution.InstitutionID, 
        Institution.Name, 
        Institution.Address, 
        Institution.AuthorsCount
    FROM Institution 
);

--################################# Topic #################################--
DROP FUNCTION IF EXISTS ListAllTopics;
------------------------------------------------------------------------------

CREATE FUNCTION ListAllTopics()
RETURNS TABLE AS
RETURN
(
    SELECT 
        Topic.TopicID, 
        Topic.Name, 
        Topic.Description,
        Topic.ArticlesCount
    FROM Topic 
);


--################################# Journal #################################--
DROP FUNCTION IF EXISTS ListAllJournals;
------------------------------------------------------------------------------

CREATE FUNCTION ListAllJournals()
RETURNS TABLE AS
RETURN
(
    SELECT 
        Journal.JournalID, 
        Journal.Name, 
        Journal.PrintISSN,
        Journal.[Url],
        Journal.ArticlesCount
    FROM Journal
);    
        
--################################# Article #################################--
DROP FUNCTION IF EXISTS ListAllArticles;
------------------------------------------------------------------------------

CREATE FUNCTION ListAllArticles()
RETURNS TABLE AS 
RETURN
(
    SELECT 
        Article.ArticleID, 
        Article.Title, 
        Article.Abstract, 
        Article.DOI,
        Journal.Name AS JournalName,
        Article.AuthorsCount
    FROM Article 
    LEFT JOIN Journal ON Journal.JournalID = Article.JournalID
);



