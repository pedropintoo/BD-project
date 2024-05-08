import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from persistence.session import create_connection
from tables.tables import Author

def read(c_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Author WHERE CustomerID = ?;", c_id)
        row = cursor.fetchone()

        return row.AuthorID, Author(
            "",
            row.AuthorName or "",
            row.Email or "",
            row.ORCID or "",
            row.InstitutionID or "",
        )    