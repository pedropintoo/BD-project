import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Article

class ArticleSimple(NamedTuple):
    ArticleID: str
    Title: str
    DOI: str

class ArticleForm(NamedTuple):
    Title: str
    Abstract: str
    DOI: str
    JournalName: str
    Volume: str
    StartPage: str
    EndPage: str



class ArticleDetails(NamedTuple):
    Title: str
    Abstract: str
    DOI: str
    StartPage: str
    EndPage: str
    JournalName: str
    Volume: str
    PublicationDate: str
    AuthorsCount: int
    AuthorsList: list[str]
    TopicsList: list[str]
    


NOT_FOUND = ArticleSimple(
            None,
            None,
            None
            )


def read(article_id: str) -> ArticleDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC ListArticleDetails @ArticleID = ?", article_id)

        article_row = cursor.fetchone()
        article_details = ArticleDetails(
            article_row[0] or "",
            article_row[1] or "",
            article_row[2] or "",
            article_row[3] or "",
            article_row[4] or "",
            article_row[5] or "",
            article_row[6] or "",
            article_row[7] or "",
            article_row[8] or 0,
            [],  # start empty
            []  # start empty
        )

        # copy the author details to a new variable
        cursor.nextset()
        authors = cursor.fetchall()
        authors_list = [author[0] for author in authors]
        article_details = article_details._replace(AuthorsList=authors_list)

        # copy the topics details to a new variable
        cursor.nextset()
        topics = cursor.fetchall()
        topics_list = [topic[0] for topic in topics]
        article_details = article_details._replace(TopicsList=topics_list)

        return article_details
    
def create(article_id, article: Article):
    with create_connection() as conn:
        cursor = conn.cursor()
        print("Try to create article")

        cursor.execute(
            """
            EXEC CreateArticle @ArticleID = ?, @Title = ?, @Abstract = ?, 
            @DOI = ?, @StartPage = ?, @EndPage = ?, @JournalName = ?, @Volume = ?
            """,
            article_id, article.Title, article.Abstract, article.DOI, article.StartPage, article.EndPage, article.JournalName, article.Volume
        )

        conn.commit()

def list_all_by_author_count():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByAuthorsCount_article;")
        rows = cursor.fetchall()
        return [ArticleSimple(
            row.ArticleID or None,
            row.Title or None,
            row.DOI or None
        ) for row in rows]
    

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByArticleTitle;")
        rows = cursor.fetchall()

        return [ArticleSimple(
            row.ArticleID or None,
            row.Title or None,
            row.DOI or None
        ) for row in rows]


def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderBySearchArticleTitle @ArticleTitle = ?", name)
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND
        
        return [ArticleSimple(
            row.ArticleID or None,
            row.Title or None,
            row.DOI or None
        ) for row in rows]
    
def delete(article_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC DeleteArticle @ArticleID = ?", article_id)
            conn.commit()    
        except Exception as e:
            print("Error: ", e)
            raise


def generate_article_id(title: str, abstract: str, doi: str, journal_name: str, volume: str, start_page: str, end_page: str) -> str:
    # Combine title, abstract, doi, journal_name, volume, start_page, end_page
    combined = f"{title}{abstract}{doi}{journal_name}{volume}{start_page}{end_page}"
    # Generate SHA-256 hash of the combined string
    hash_object = hashlib.sha256(combined.encode())
    # Return the first 10 characters of the hash
    article_id = hash_object.hexdigest()[:10]
    return article_id

def update(article_id: str, article: Article):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            EXEC UpdateArticle @ArticleID = ?, @Title = ?, @Abstract = ?, @DOI = ?, 
            @StartPage = ?, @EndPage = ?, @JournalName = ?, @Volume = ?
            """,
            article_id,
            article.Title if article.Title != "" else None,
            article.Abstract if article.Abstract != "" else None,
            article.DOI if article.DOI != "" else None,
            article.StartPage if article.StartPage != "" else None,
            article.EndPage if article.EndPage != "" else None,
            article.JournalName if article.JournalName != "" else None,
            article.Volume if article.Volume != "" else None
        )
        conn.commit()
    
