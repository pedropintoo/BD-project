from typing import NamedTuple

# external dependency
tables =  [
    "Comment",
    "Wrote_by",
    "Author",
    "Read_by",
    "Favorite_Article",
    "Interested_in",
    "Favorite_Journal",
    "[User]",
    "Institution",
    "Has_Keywords",
    "Keyword",
    "Cited_by",
    "Belongs_to",
    "Article",
    "JournalVolume",
    "Journal",
    "Topic"
]

class Author(NamedTuple):
    AuthorID: str
    Name: str
    Url: str
    ORCID: str
    InstitutionID: str
    ArticlesCount: int

class Institution(NamedTuple):
    InstitutionID: str
    Name: str
    Address: str
    AuthorsCount: int

class Topic(NamedTuple):
    TopicID: str
    Name: str
    Description: str    

class Article(NamedTuple):
    ArticleID: str
    Title: str
    Abstract: str
    DOI: str
    StartPage: int
    EndPage: int
    JournalID: str
    Volume: int    

class Journal(NamedTuple):
    JournalID: str
    Name: str
    PrintISSN: str
    EletronicISSN: str
    Url: int
    Publisher: int  

class JournalVolume(NamedTuple):
    JournalID: str
    Volume: str  
    PublicationDate: str   