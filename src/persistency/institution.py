import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Institution

NOT_FOUND = Institution(
            None,
            None,
            None,
            )

class Institution(NamedTuple):
    InstitutionID: str
    Name: str
    Address: str

def read(institution_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Institution WHERE InstitutionID = ?;", institution_id)
        row = cursor.fetchone()

        return Institution(
            row.InstitutionID or None,
            row.Name or None,
            row.Address or None,
        )

def create(institution: Institution):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Institution (InstitutionID, Name, Address)
            VALUES (?, ?, ?);
            """,
            (institution.InstitutionID, institution.Name, institution.Address)
        )
        conn.commit()

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Institution;")
        rows = cursor.fetchall()

        return [Institution(
            row.InstitutionID or None,
            row.Name or None,
            row.Address or None,
        ) for row in rows]
       
def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Institution WHERE Name LIKE ?;", '%'+name+'%')
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [Institution(
            row.InstitutionID or None,
            row.Name or None,
            row.Address or None,
        ) for row in rows]
    
def delete(institution_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC DeleteInstitutionAndUpdateAuthors @InstitutionID = ?", institution_id)
            cursor.commit()
        except Exception as e:
            print("Error:", e)
            raise

def generate_institution_id(name: str, address: str) -> str:
    # Combine name and institution_id
    combined = f"{name}{address}"
    # Generate SHA-256 hash of the combined string
    hash_object = hashlib.sha256(combined.encode())
    # Get the first 10 characters of the hex digest
    institution_id = hash_object.hexdigest()[:10]
    return institution_id


# Testing purpose
def search_institution_by_prefix(prefix: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT Name FROM Institution WHERE Name LIKE ?;"
        cursor.execute(query, (prefix + '%',))
        results = cursor.fetchall()
        return [row[0] for row in results] 