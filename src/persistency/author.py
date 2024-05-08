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

def read(c_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Author WHERE CustomerID = ?;", c_id)
        row = cursor.fetchone()

        return Author(
            row.AuthorID or "Not found",
            row.Name or "Not found",
            row.Email or "Not found",
            row.ORCID or "Not found",
            row.InstitutionID or "Not found",
        )

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Author;")
        rows = cursor.fetchall()

        return [Author(
            row.AuthorID or "Not found",
            row.Name or "Not found",
            row.Email or "Not found",
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
            row.Email or "Not found",
            row.ORCID or "Not found",
            row.InstitutionID or "Not found",
        ) for row in rows]