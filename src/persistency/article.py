import sys
sys.path.append('.')

import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Article

NOT_FOUND = Article(
            "Not found",
            "Not found",
            "Not found",
            "Not found",
            "Not found",
            "Not found",
            "Not found",
            "Not found"
            )

def read(c_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Article WHERE ArticleID = ?;", c_id)
        row = cursor.fetchone()

        return Article(
            row.ArticleID or "Not found",
            row.Title or "Not found",
            row.Abstract or "Not found",
            row.DOI or "Not found",
            row.StartPage or "Not found",
            row.EndPage or "Not found",
            row.JournalID or "Not found",
            row.Volume or "Not found"
        )

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Article;")
        rows = cursor.fetchall()

        return [Article(
            row.ArticleID or "Not found",
            row.Title or "Not found",
            row.Abstract or "Not found",
            row.DOI or "Not found",
            row.StartPage or "Not found",
            row.EndPage or "Not found",
            row.JournalID or "Not found",
            row.Volume or "Not found"
        ) for row in rows]
       
def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Article WHERE Title LIKE ?;", '%'+name+'%')
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [Article(
            row.ArticleID or "Not found",
            row.Title or "Not found",
            row.Abstract or "Not found",
            row.DOI or "Not found",
            row.StartPage or "Not found",
            row.EndPage or "Not found",
            row.JournalID or "Not found",
            row.Volume or "Not found"
        ) for row in rows]