import sys
sys.path.append('.')

import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Topic

NOT_FOUND = Topic(
            "Not found",
            "Not found",
            "Not found"
            )

def read(c_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Topic WHERE TopicID = ?;", c_id)
        row = cursor.fetchone()

        return Topic(
            row.TopicID or "Not found",
            row.Name or "Not found",
            row.Description or "Not found"
        )

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Topic;")
        rows = cursor.fetchall()

        return [Topic(
            row.TopicID or "Not found",
            row.Name or "Not found",
            row.Description or "Not found"
        ) for row in rows]
       
def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Topic WHERE Name LIKE ?;", '%'+name+'%')
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [Topic(
            row.TopicID or "Not found",
            row.Name or "Not found",
            row.Description or "Not found"
        ) for row in rows]