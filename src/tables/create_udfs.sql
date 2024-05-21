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