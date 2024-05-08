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
    "Article",
    "JournalVolume",
    "Belongs_to",
    "Journal",
    "Topic"
]

class Author(NamedTuple):
    AuthorID: str
    Name: str
    Email: str
    ORCID: str
    InstitutionID: str

class Institution(NamedTuple):
    InstitutionID: str
    Name: str
    Address: str

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