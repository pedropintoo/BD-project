-- # Authors with None are not considered in the list

-- Author --
DROP FUNCTION IF EXISTS ListAllAuthors;
DROP PROCEDURE IF EXISTS OrderByAuthorName;
DROP PROCEDURE IF EXISTS OrderBySearchAuthorName;
DROP PROCEDURE IF EXISTS ListAllAuthorsDetails;
DROP PROCEDURE IF EXISTS GetInstitutionIDByName;
DROP PROCEDURE IF EXISTS DeleteAuthor;
DROP PROCEDURE IF EXISTS OrderByArticlesCount;  
DROP TRIGGER IF EXISTS trg_UpdateArticlesCount_Insert;
DROP TRIGGER IF EXISTS trg_UpdateArticlesCount_Delete;
DROP TRIGGER IF EXISTS trg_UpdateArticlesCount_Update;
DROP INDEX IDX_Author_Name ON Author;
DROP INDEX IDX_Author_ArticlesCount ON Author;

-- Institution --
DROP FUNCTION IF EXISTS ListAllInstitutions;
DROP PROCEDURE IF EXISTS OrderByInstitutionName;
DROP PROCEDURE IF EXISTS OrderBySearchInstitutionName;
DROP PROCEDURE IF EXISTS ListAllInstitutionsDetails;
DROP PROCEDURE IF EXISTS DeleteInstitutionAndUpdateAuthors;
DROP PROCEDURE IF EXISTS OrderByAuthorsCount;
DROP TRIGGER IF EXISTS trg_UpdateAuthorsCount_Insert;
DROP TRIGGER IF EXISTS trg_UpdateAuthorsCount_Delete;
DROP TRIGGER IF EXISTS trg_UpdateAuthorsCount_Update;
DROP INDEX IDX_Institution_Name ON Institution;
DROP INDEX IDX_Institution_AuthorsCount ON Institution;
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
        Author.ArticlesCount
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
        Institution.Name AS InstitutionName,
        Author.ArticlesCount
    FROM Author 
    LEFT JOIN Institution ON Institution.InstitutionID = Author.InstitutionID
);


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


-- Trigger para atualizar ArticlesCount após inserção em Wrote_by
CREATE TRIGGER trg_UpdateArticlesCount_Insert
ON Wrote_by
AFTER INSERT
AS
BEGIN
    UPDATE Author
    SET ArticlesCount = (SELECT COUNT(*) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID)
    FROM Author
    INNER JOIN inserted i ON Author.AuthorID = i.AuthorID
END;

-- Trigger para atualizar ArticlesCount após deleção de Wrote_by
CREATE TRIGGER trg_UpdateArticlesCount_Delete
ON Wrote_by
AFTER DELETE
AS
BEGIN
    UPDATE Author
    SET ArticlesCount = (SELECT COUNT(*) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID)
    FROM Author
    INNER JOIN deleted d ON Author.AuthorID = d.AuthorID
END;

-- Trigger para atualizar ArticlesCount após atualização de Wrote_by
CREATE TRIGGER trg_UpdateArticlesCount_Update
ON Wrote_by
AFTER UPDATE
AS
BEGIN
    UPDATE Author
    SET ArticlesCount = (SELECT COUNT(*) FROM Wrote_by WHERE Wrote_by.AuthorID = Author.AuthorID)
    FROM Author
    INNER JOIN inserted i ON Author.AuthorID = i.AuthorID
END;

--------------------------- Institution ---------------------------
-- Adicionar índice não-clusterizado para a coluna Name para acelerar a pesquisa
CREATE NONCLUSTERED INDEX IDX_Institution_Name
ON Institution (Name);

--- Index AuthorsCount
CREATE NONCLUSTERED INDEX IDX_Institution_AuthorsCount
ON Institution (AuthorsCount);

CREATE PROCEDURE ListAllInstitutionsDetails
    @InstitutionID VARCHAR(10)
AS
BEGIN
    SELECT 
        Institution.InstitutionID, 
        Institution.Name, 
        Institution.Address,
        Institution.AuthorsCount
    FROM Institution
    WHERE Institution.InstitutionID = @InstitutionID

    -- Segundo conjunto de resultados: Lista de Autores
    SELECT 
        Author.Name 
    FROM 
        Author
    WHERE 
        Author.InstitutionID = @InstitutionID
END;

CREATE FUNCTION ListAllInstitutions()
RETURNS TABLE
AS
RETURN
(
    SELECT 
        Institution.InstitutionID, 
        Institution.Name, 
        Institution.Address, 
        Institution.AuthorsCount
    FROM Institution 
);


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


-- Trigger para atualizar AuthorsCount após inserção em Author
CREATE TRIGGER trg_UpdateAuthorsCount_Insert
ON Author
AFTER INSERT
AS
BEGIN
    UPDATE Institution
    SET AuthorsCount = (SELECT COUNT(*) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN inserted i ON Institution.InstitutionID = i.InstitutionID
END;

-- Trigger para atualizar AuthorsCount após deleção em Author
CREATE TRIGGER trg_UpdateAuthorsCount_Delete
ON Author
AFTER DELETE
AS
BEGIN
    UPDATE Institution
    SET AuthorsCount = (SELECT COUNT(*) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN deleted i ON Institution.InstitutionID = i.InstitutionID
END;


-- Trigger para atualizar AuthorsCount após atualização em Author
CREATE TRIGGER trg_UpdateAuthorsCount_Update
ON Author
AFTER UPDATE
AS
BEGIN
    UPDATE Institution
    SET AuthorsCount = (SELECT COUNT(*) FROM Author WHERE Author.InstitutionID = Institution.InstitutionID)
    FROM Institution
    INNER JOIN inserted i ON Institution.InstitutionID = i.InstitutionID
END;