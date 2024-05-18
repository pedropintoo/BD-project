ALTER PROCEDURE ListAllAuthors
AS
BEGIN
    SELECT Author.AuthorID, Author.Name, Author.[Url], Institution.Name as InstitutionName
    FROM Author 
    INNER JOIN Institution on Institution.InstitutionID = Author.InstitutionID
    ORDER BY Author.Name
END;

ALTER PROCEDURE ListAllAuthorsDetails
    @AuthorID VARCHAR(10)
AS
BEGIN
    SELECT 
        Author.AuthorID, 
        Author.Name, 
        Author.[Url], 
        Author.ORCID, 
        Author.InstitutionID,
        Institution.Name AS InstitutionName
    FROM Author
    INNER JOIN Institution ON Institution.InstitutionID = Author.InstitutionID
    WHERE Author.AuthorID = @AuthorID
END;


ALTER PROCEDURE GetInstitutionIDByName
    @InstitutionName VARCHAR(300)
AS
BEGIN
    SELECT InstitutionID
    FROM Institution
    WHERE [Name] = @InstitutionName
END;
