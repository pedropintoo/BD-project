import sys
sys.path.append('.')

import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Journal

NOT_FOUND = Journal(
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
        cursor.execute("SELECT * FROM Journal WHERE JournalID = ?;", c_id)
        row = cursor.fetchone()

        return Journal(
            row.JournalID or "Not found",
            row.Name or "Not found",
            row.PrintISSN or "Not found",
            row.EletronicISSN or "Not found",
            row.Url or "Not found",
            row.Publisher or "Not found"
        )

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Journal;")
        rows = cursor.fetchall()

        return [Journal(
            row.JournalID or "Not found",
            row.Name or "Not found",
            row.PrintISSN or "Not found",
            row.EletronicISSN or "Not found",
            row.Url or "Not found",
            row.Publisher or "Not found"
        ) for row in rows]
       
def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Journal WHERE Name LIKE ?;", '%'+name+'%')
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [Journal(
            row.JournalID or "Not found",
            row.Name or "Not found",
            row.PrintISSN or "Not found",
            row.EletronicISSN or "Not found",
            row.Url or "Not found",
            row.Publisher or "Not found"
        ) for row in rows]