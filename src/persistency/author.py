import sys
sys.path.append('.')

import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Author

NOT_FOUND = Author(
            "Not found",
            "Not found",
            "Not found",
            "Not found",
            "Not found"
            )

class Author(NamedTuple):
    AuthorID: str
    Name: str
    Url: str
    ORCID: str
    InstitutionID: str

def read(author_id: str) -> Author:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Author WHERE AuthorID = ?;", (author_id,))
        row = cursor.fetchone()
        if row:
            return Author(
                row[0] or "Not found",
                row[1] or "Not found",
                row[2] or "Not found",
                row[3] or "Not found",
                row[4] or "Not found"
            )
        else:
            return Author(
                "Not found",
                "Not found",
                "Not found",
                "Not found",
                "Not found"
            )

def create(author: Author):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Author (AuthorID, Name, Url, ORCID, InstitutionID)
            VALUES (?, ?, ?, ?, ?);
            """,
            (author.AuthorID, author.Name, author.Url, author.ORCID, author.InstitutionID)
        )
        conn.commit()

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Author;")
        rows = cursor.fetchall()

        return [Author(
            row.AuthorID or "Not found",
            row.Name or "Not found",
            row.Url or "Not found",
            row.ORCID or "Not found",
            row.InstitutionID or "Not found",
        ) for row in rows]
       
def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Author WHERE Name LIKE ?;", '%'+name+'%')
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [Author(
            row.AuthorID or "Not found",
            row.Name or "Not found",
            row.Url or "Not found",
            row.ORCID or "Not found",
            row.InstitutionID or "Not found",
        ) for row in rows]
    
def delete(c_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE Author WHERE AuthorID = ?;", c_id)
            cursor.commit()
        except IntegrityError as ex:
            if ex.args[0] == "23000":
                raise Exception(f"Author {c_id} cannot be deleted. Probably has orders.") from ex

def update(author_id: str, author: CustomerDetails):