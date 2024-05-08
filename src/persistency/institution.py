import sys
sys.path.append('.')

import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Institution

NOT_FOUND = Institution(
            "Not found",
            "Not found",
            "Not found",
            )

def read(c_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Institution WHERE InstitutionID = ?;", c_id)
        row = cursor.fetchone()

        return Institution(
            row.InstitutionID or "Not found",
            row.Name or "Not found",
            row.Address or "Not found",
        )

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Institution;")
        rows = cursor.fetchall()

        return [Institution(
            row.InstitutionID or "Not found",
            row.Name or "Not found",
            row.Address or "Not found",
        ) for row in rows]
       
def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Institution WHERE Name LIKE ?;", '%'+name+'%')
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [Institution(
            row.InstitutionID or "Not found",
            row.Name or "Not found",
            row.Address or "Not found",
        ) for row in rows]