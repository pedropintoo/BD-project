-- # Authors with None are not considered in the list
DROP FUNCTION IF EXISTS ListAllAuthors;
DROP PROCEDURE IF EXISTS OrderByAuthorName;
DROP PROCEDURE IF EXISTS OrderBySearchAuthorName;
DROP PROCEDURE IF EXISTS ListAllAuthorsDetails;
DROP PROCEDURE IF EXISTS GetInstitutionIDByName;
DROP PROCEDURE IF EXISTS DeleteInstitutionAndUpdateAuthors;
DROP PROCEDURE IF EXISTS DeleteAuthor;

--------------------------- Author ---------------------------

-- Adicionar índice não-clusterizado para a coluna Name para acelerar a pesquisa
CREATE NONCLUSTERED INDEX IDX_Author_Name
ON Author (Name);

--- Index ArticlesCount
CREATE NONCLUSTERED INDEX IDX_Author_ArticlesCount
ON Author (ArticlesCount);

CREATE PROCEDURE ListAllAuthorsDetails
    @AuthorID VARCHAR(10)
AS
BEGIN
    SELECT 
        Author.AuthorID, 
        Author.Name, 
        Author.[Url], 
        Author.ORCID, 
        Author.InstitutionID,
        Institution.Name AS InstitutionName,
        (SELECT COUNT(*) 
         FROM Wrote_by 
         WHERE Wrote_by.AuthorID = Author.AuthorID) AS ArticlesCount
    FROM Author
    LEFT JOIN Institution ON Institution.InstitutionID = Author.InstitutionID
    WHERE Author.AuthorID = @AuthorID

    -- Segundo conjunto de resultados: Lista de Artigos
    SELECT 
        Article.Title 
    FROM Wrote_by 
    INNER JOIN Article ON Wrote_by.ArticleID = Article.ArticleID
    WHERE Wrote_by.AuthorID = @AuthorID
END;


CREATE FUNCTION ListAllAuthors()
RETURNS TABLE
AS
RETURN
(
    SELECT 
        Author.AuthorID, 
        Author.Name, 
        Author.[Url], 
        Institution.Name AS InstitutionName
    FROM Author 
    LEFT JOIN Institution ON Institution.InstitutionID = Author.InstitutionID
);


CREATE PROCEDURE OrderByAuthorName 
AS
BEGIN
    SELECT * FROM ListAllAuthors()
    ORDER BY [Name]
END;

CREATE PROCEDURE OrderBySearchAuthorName (@AuthorName NVARCHAR(50))
AS
BEGIN
    SELECT * FROM ListAllAuthors() 
    WHERE [Name] LIKE '%' + @AuthorName + '%'
    ORDER BY [Name]
END;


-- Delele Author with AuthorID and Entries in Wrote_by
CREATE PROCEDURE DeleteAuthor
    @AuthorID VARCHAR(10)
AS
BEGIN
    BEGIN TRANSACTION

    BEGIN TRY
        -- Remover os registros relacionados na tabela Wrote_by
        DELETE FROM Wrote_by
        WHERE AuthorID = @AuthorID

        -- Remover o autor
        DELETE FROM Author
        WHERE AuthorID = @AuthorID

        -- Commit da transação
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        -- Rollback da transação em caso de erro
        ROLLBACK TRANSACTION
        -- Rethrow o erro
        THROW
    END CATCH
END;



CREATE PROCEDURE GetInstitutionIDByName
    @InstitutionName VARCHAR(300)
AS
BEGIN
    SELECT InstitutionID
    FROM Institution
    WHERE [Name] = @InstitutionName
END;


--------------------------- Institution ---------------------------

CREATE PROCEDURE DeleteInstitutionAndUpdateAuthors
    @InstitutionID VARCHAR(10)
AS
BEGIN
    -- Iniciar uma transação
    BEGIN TRANSACTION

    BEGIN TRY
        -- Definir InstitutionID como NULL para autores que referenciam esta instituição
        UPDATE Author
        SET InstitutionID = NULL
        WHERE InstitutionID = @InstitutionID

        -- Deletar a instituição
        DELETE FROM Institution
        WHERE InstitutionID = @InstitutionID

        -- Commit da transação
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        -- Rollback da transação em caso de erro
        ROLLBACK TRANSACTION

        -- Lançar o erro capturado
        THROW
    END CATCH
END;
