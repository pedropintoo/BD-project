GO
USE p5g1
GO

CREATE TABLE Topic(
    TopicID             INT             NOT NULL,
    [Name]              VARCHAR(50)     NOT NULL,
    [Description]       VARCHAR(500),
    PRIMARY KEY (TopicID),
    UNIQUE ([Name])
)

CREATE TABLE Journal(
    JournalID           INT             NOT NULL,
    [Name]              VARCHAR(100)    NOT NULL,
    PrintISSN           VARCHAR(9),
    EletronicISSN       VARCHAR(9),
    Frequency           VARCHAR(20),
    Publisher           VARCHAR(50),
    PRIMARY KEY (JournalID),
    UNIQUE ([Name], Publisher),
    UNIQUE (PrintISSN),
    UNIQUE (EletronicISSN)
)

CREATE TABLE Belongs_to(
    TopicID              INT            NOT NULL,
    JournalID            INT            NOT NULL,
    PRIMARY KEY (TopicID,JournalID),
    FOREIGN KEY (TopicID) REFERENCES Topic(TopicID),
    FOREIGN KEY (JournalID) REFERENCES Journal(JournalID)
)

CREATE TABLE JournalVolume(
    JournalID           INT             NOT NULL,
    Volume              INT             NOT NULL,
    PublicationDate     DATE,
    PRIMARY KEY (JournalID,Volume),
    FOREIGN KEY (JournalID) REFERENCES Journal(JournalID)
)

CREATE TABLE Article(
    ArticleID           INT             NOT NULL,
    Title               VARCHAR(100)    NOT NULL,
    Abstract            VARCHAR(1250),
    DOI                 VARCHAR(50)     NOT NULL,
    StartPage           INT,
    EndPage             INT,
    JournalID           INT             NOT NULL,
    Volume              INT             NOT NULL,
    PRIMARY KEY (ArticleID),
    FOREIGN KEY (JournalID,Volume) REFERENCES JournalVolume(JournalID,Volume),
    UNIQUE (DOI),
    UNIQUE (JournalID, Volume, StartPage, EndPage)
)

CREATE TABLE Cited_by(
    CitedArticleID      INT             NOT NULL,
    CitingArticleID     INT             NOT NULL,
    PRIMARY KEY (CitedArticleID,CitingArticleID),
    FOREIGN KEY (CitedArticleID) REFERENCES Article(ArticleID),
    FOREIGN KEY (CitingArticleID) REFERENCES Article(ArticleID)
)

CREATE TABLE Keyword(
    [KeywordName]              VARCHAR(50)     NOT NULL,
    PRIMARY KEY ([KeywordName])
)

CREATE TABLE Has_Keywords(
    ArticleID           INT             NOT NULL,
    KeywordName         VARCHAR(50)     NOT NULL,
    PRIMARY KEY (ArticleID,KeywordName),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID),
    FOREIGN KEY (KeywordName) REFERENCES Keyword(KeywordName)
)

CREATE TABLE Institution(
    InstitutionID       INT             NOT NULL,
    [Name]              VARCHAR(50)     NOT NULL,
    [Address]           VARCHAR(100),
    PRIMARY KEY (InstitutionID),
    UNIQUE ([Name])
)

CREATE TABLE [User] (
    UserID              INT             NOT NULL,
    [Name]              VARCHAR(50)     NOT NULL,
    Email               VARCHAR(320)    NOT NULL,
    [Password]          VARCHAR(30)     NOT NULL,
    InstitutionID       INT,
    PRIMARY KEY (UserID),
    FOREIGN KEY (InstitutionID) REFERENCES Institution(InstitutionID),
    UNIQUE (Email)
)

CREATE TABLE Favorite_Journal (
    JournalID           INT             NOT NULL,
    UserID              INT             NOT NULL,
    PRIMARY KEY (JournalID,UserID),
    FOREIGN KEY (JournalID) REFERENCES Journal(JournalID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
)

CREATE TABLE Interested_in (
    TopicID             INT             NOT NULL,
    UserID              INT             NOT NULL,
    PRIMARY KEY (TopicID,UserID),
    FOREIGN KEY (TopicID) REFERENCES Topic(TopicID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
)

CREATE TABLE Favorite_Article (
    ArticleID           INT             NOT NULL,
    UserID              INT             NOT NULL,
    PRIMARY KEY (ArticleID,UserID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID)
)

CREATE TABLE Read_by (
    ArticleID           INT             NOT NULL,
    UserID              INT             NOT NULL,
    PRIMARY KEY (ArticleID,UserID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID)
)

CREATE TABLE Author (
    AuthorID            INT             NOT NULL,
    [Name]              VARCHAR(50)     NOT NULL,
    Email               VARCHAR(320),
    ORCID               VARCHAR(19),
    InstitutionID       INT,
    PRIMARY KEY (AuthorID),
    FOREIGN KEY (InstitutionID) REFERENCES Institution(InstitutionID),
    UNIQUE (Email),
    UNIQUE (ORCID)
)

CREATE TABLE Wrote_by (
    ArticleID           INT             NOT NULL,
    AuthorID            INT             NOT NULL,
    PRIMARY KEY (ArticleID,AuthorID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID),
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID)
)
CREATE TABLE Comment (
    ArticleID           INT             NOT NULL,
    UserID              INT             NOT NULL,
    CommentID           INT             NOT NULL,
    Content             VARCHAR(500)    NOT NULL,
    [Date]              DATE,
    PRIMARY KEY (ArticleID,UserID,CommentID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
)