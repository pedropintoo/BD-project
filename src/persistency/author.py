import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Author

class AuthorSimple(NamedTuple):
    AuthorID: str
    Name: str
    Url: str
    InstitutionName: str

class AuthorForm(NamedTuple):
    Name: str
    Url: str
    ORCID: str
    InstitutionName: str

class AuthorDetails(NamedTuple):
    Name: str
    Url: str
    ORCID: str
    InstitutionName: str
    ArticlesCount: int
    ArticlesList: list[str] 

NOT_FOUND = AuthorSimple(
            None,
            None,
            None,
            None
            )
    

def read(author_id: str) -> AuthorDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC ListAuthorDetails @AuthorID = ?", author_id)

        author_row = cursor.fetchone()
        author_details = AuthorDetails(
            author_row[0] or "",
            author_row[1] or "",
            author_row[2] or "",
            author_row[3] or "",
            author_row[4] or 0,
            []  # start empty
        )

        # copy the author details to a new variable
        cursor.nextset()  
        articles = cursor.fetchall()
        articles_list = [article[0] for article in articles]
        author_details = author_details._replace(ArticlesList=articles_list)

        return author_details


def create(author_id, author):
    with create_connection() as conn:
        cursor = conn.cursor()
        print("Try to create author")

        cursor.execute(
            "EXEC CreateAuthor @AuthorID = ?, @Name = ?, @Url = ?, @ORCID = ?, @InstitutionName = ?",
            author_id, author.Name, author.Url, author.ORCID, author.InstitutionName
        )
        
        conn.commit()


def list_all_by_article_count():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByArticlesCount;")
        rows = cursor.fetchall()
        return [AuthorSimple(
            row.AuthorID or None,
            row.Name or None,
            row.Url or None,
            row.InstitutionName or None
        ) for row in rows]

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByAuthorName;")
        rows = cursor.fetchall()
        return [AuthorSimple(
            row.AuthorID or None,
            row.Name or None,
            row.Url or None,
            row.InstitutionName or None
        ) for row in rows]

def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderBySearchAuthorName @AuthorName = ?", name)
        rows = cursor.fetchall()
        
        if rows == None:
            return NOT_FOUND

        return [AuthorSimple(
            row.AuthorID or None,
            row.Name or None,
            row.Url or None,
            row.InstitutionName or None
        ) for row in rows]

    
def delete(author_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC DeleteAuthor @AuthorID = ?", author_id)
            cursor.commit()
        except Exception as e:
            print("Error:", e)
            raise

def generate_author_id(name: str, url: str, orcid: str, institution_name: str) -> str:
    # Combine name and institution_id
    combined = f"{name}{url}{orcid}{institution_name}"
    # Generate SHA-256 hash of the combined string
    hash_object = hashlib.sha256(combined.encode())
    # Get the first 10 characters of the hex digest
    author_id = hash_object.hexdigest()[:10]
    return author_id

                
def update(author_id: str, author: Author):
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            EXEC UpdateAuthor 
            @AuthorID = ?, @Name = ?, @Url = ?, @ORCID = ?, @InstitutionName = ?;
            """,
            author_id,
            author.Name if author.Name != "" else None,
            author.Url if author.Url != "" else None,
            author.ORCID if author.ORCID != "" else None,
            author.InstitutionName if author.InstitutionName != "" else None,
        )
        conn.commit()

