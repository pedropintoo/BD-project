IF OBJECT_ID('Topic') IS NULL
BEGIN
CREATE TABLE Topic(
    TopicID             VARCHAR(10)     NOT NULL,
    [Name]              VARCHAR(50)     NOT NULL,
    [Description]       VARCHAR(500),
    ArticlesCount               INT,
    PRIMARY KEY (TopicID),
    UNIQUE ([Name])
)
END;

IF OBJECT_ID('Journal') IS NULL
BEGIN
CREATE TABLE Journal(
    JournalID           VARCHAR(40)     NOT NULL,
    [Name]              VARCHAR(100),
    PrintISSN           VARCHAR(9),
    EletronicISSN       VARCHAR(9),
    [Url]               VARCHAR(100),
    Publisher           VARCHAR(50),
    ArticlesCount               INT,
    PRIMARY KEY (JournalID),
)
END;

IF OBJECT_ID('JournalVolume') IS NULL
BEGIN
CREATE TABLE JournalVolume(
    JournalID           VARCHAR(40)     NOT NULL,
    Volume              INT             NOT NULL,
    PublicationDate     DATE,
    PRIMARY KEY (JournalID,Volume),
    FOREIGN KEY (JournalID) REFERENCES Journal(JournalID)
)
END;

IF OBJECT_ID('Article') IS NULL
BEGIN
CREATE TABLE Article(
    ArticleID           VARCHAR(10)     NOT NULL,
    Title              NVARCHAR(500)    NOT NULL,
    Abstract            VARCHAR(1250),
    DOI                 VARCHAR(50),
    StartPage           INT,
    EndPage             INT,
    JournalID           VARCHAR(40),
    Volume              INT,
    PRIMARY KEY (ArticleID),
    FOREIGN KEY (JournalID,Volume) REFERENCES JournalVolume(JournalID,Volume),
)
END;

IF OBJECT_ID('Belongs_to') IS NULL
BEGIN
CREATE TABLE Belongs_to(
    TopicID             VARCHAR(10)     NOT NULL,
    ArticleID           VARCHAR(10)     NOT NULL,
    PRIMARY KEY (TopicID,ArticleID),
    FOREIGN KEY (TopicID) REFERENCES Topic(TopicID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID)
)
END;

IF OBJECT_ID('Cited_by') IS NULL
BEGIN
CREATE TABLE Cited_by(
    CitedArticleID      VARCHAR(10)     NOT NULL,
    CitingArticleID     VARCHAR(10)     NOT NULL,
    PRIMARY KEY (CitedArticleID,CitingArticleID),
    FOREIGN KEY (CitedArticleID) REFERENCES Article(ArticleID),
    FOREIGN KEY (CitingArticleID) REFERENCES Article(ArticleID)
)
END;

IF OBJECT_ID('Keyword') IS NULL
BEGIN
CREATE TABLE Keyword(
    [KeywordName]       VARCHAR(50)     NOT NULL,
    PRIMARY KEY ([KeywordName])
)
END;

IF OBJECT_ID('Has_Keywords') IS NULL
BEGIN
CREATE TABLE Has_Keywords(
    ArticleID           VARCHAR(10)     NOT NULL,
    KeywordName         VARCHAR(50)     NOT NULL,
    PRIMARY KEY (ArticleID,KeywordName),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID),
    FOREIGN KEY (KeywordName) REFERENCES Keyword(KeywordName)
)
END;

IF OBJECT_ID('Institution') IS NULL
BEGIN
CREATE TABLE Institution(
    InstitutionID       VARCHAR(10)     NOT NULL,
    [Name]              VARCHAR(300)     NOT NULL,
    [Address]           VARCHAR(100),
    AuthorsCount               INT,
    PRIMARY KEY (InstitutionID),
    UNIQUE ([Name])
)
END;

IF OBJECT_ID('User') IS NULL
BEGIN
CREATE TABLE [User] (
    UserID              VARCHAR(10)     NOT NULL,
    [Name]              VARCHAR(50)     NOT NULL,
    Email               VARCHAR(320)    NOT NULL,
    [Password]          VARCHAR(30)     NOT NULL,
    InstitutionID       VARCHAR(10),
    PRIMARY KEY (UserID),
    FOREIGN KEY (InstitutionID) REFERENCES Institution(InstitutionID),
    UNIQUE (Email)
)
END;

IF OBJECT_ID('Favorite_Journal') IS NULL
BEGIN
CREATE TABLE Favorite_Journal (
    JournalID           VARCHAR(40)     NOT NULL,
    UserID              VARCHAR(10)     NOT NULL,
    PRIMARY KEY (JournalID,UserID),
    FOREIGN KEY (JournalID) REFERENCES Journal(JournalID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
)
END;

IF OBJECT_ID('Interested_in') IS NULL
BEGIN
CREATE TABLE Interested_in (
    TopicID             VARCHAR(10)     NOT NULL,
    UserID              VARCHAR(10)     NOT NULL,
    PRIMARY KEY (TopicID,UserID),
    FOREIGN KEY (TopicID) REFERENCES Topic(TopicID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
)
END;

IF OBJECT_ID('Favorite_Article') IS NULL
BEGIN
CREATE TABLE Favorite_Article (
    ArticleID           VARCHAR(10)     NOT NULL,
    UserID              VARCHAR(10)     NOT NULL,
    PRIMARY KEY (ArticleID,UserID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID)
)
END;

IF OBJECT_ID('Read_by') IS NULL
BEGIN
CREATE TABLE Read_by (
    ArticleID           VARCHAR(10)     NOT NULL,
    UserID              VARCHAR(10)     NOT NULL,
    PRIMARY KEY (ArticleID,UserID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID)
)
END;

IF OBJECT_ID('Author') IS NULL
BEGIN
CREATE TABLE Author (
    AuthorID            VARCHAR(10)     NOT NULL,
    [Name]             NVARCHAR(50)     NOT NULL,
    [Url]               VARCHAR(100),
    ORCID               VARCHAR(19),
    InstitutionID       VARCHAR(10),
    ArticlesCount               INT,
    PRIMARY KEY (AuthorID),
    FOREIGN KEY (InstitutionID) REFERENCES Institution(InstitutionID),
)
END;

IF OBJECT_ID('Wrote_by') IS NULL
BEGIN
CREATE TABLE Wrote_by (
    ArticleID           VARCHAR(10)     NOT NULL,
    AuthorID            VARCHAR(10)     NOT NULL,
    PRIMARY KEY (ArticleID,AuthorID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID),
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID)
)
END;

IF OBJECT_ID('Comment') IS NULL
BEGIN
CREATE TABLE Comment (
    ArticleID           VARCHAR(10)     NOT NULL,
    UserID              VARCHAR(10)     NOT NULL,
    CommentID           VARCHAR(10)     NOT NULL,
    Content             VARCHAR(500)    NOT NULL,
    [Date]              DATE,
    PRIMARY KEY (ArticleID,UserID,CommentID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
)
END;



