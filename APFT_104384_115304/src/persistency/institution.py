import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Institution

class InstitutionSimple(NamedTuple):
    InstitutionID: str
    Name: str
    Address: str

class InstitutionForm(NamedTuple):
    Name: str
    Address: str

class InstitutionDetails(NamedTuple):
    Name: str
    Address: str
    AuthorsCount: int
    AuthorsList: list[str]

NOT_FOUND = InstitutionSimple(
            None,
            None,
            None,
            )


def read(institution_id: str) -> InstitutionDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC ListInstitutionDetails @InstitutionID = ?", institution_id)

        institution_row = cursor.fetchone()
        institution_details = InstitutionDetails(
            institution_row[0] or "",
            institution_row[1] or "",
            institution_row[2] or 0,
            [] # start empty
        )

        # copy the author details to a new variable
        cursor.nextset() 
        authors = cursor.fetchall()
        authors_list = [author[0] for author in authors]
        institution_details = institution_details._replace(AuthorsList=authors_list)

        return institution_details

def create(institution_id, institution: Institution):
    with create_connection() as conn:
        cursor = conn.cursor()
        print("Try to create institution")

        cursor.execute(
            """
            EXEC CreateInstitution @InstitutionID = ?, @Name = ?, @Address = ?
            """,
            (institution_id, institution.Name, institution.Address)
        )

        conn.commit()


def list_all_by_author_count():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByAuthorsCount;")
        rows = cursor.fetchall()
        return [InstitutionSimple(
            row.InstitutionID or None,
            row.Name or None,
            row.Address or None
        ) for row in rows]

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByInstitutionName;")
        rows = cursor.fetchall()

        return [InstitutionSimple(
            row.InstitutionID or None,
            row.Name or None,
            row.Address or None,
        ) for row in rows]
       
def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderBySearchInstitutionName @InstitutionName = ?", name)
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [InstitutionSimple(
            row.InstitutionID or None,
            row.Name or None,
            row.Address or None,
        ) for row in rows]
    
def delete(institution_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC DeleteInstitution @InstitutionID = ?", institution_id)
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


def update(institution_id: str, institution: Institution):
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            EXEC UpdateInstitution 
            @InstitutionID = ?, @Name = ?, @Address = ?;
            """,
            institution_id,
            institution.Name if institution.Name != "" else None,
            institution.Address if institution.Address != "" else None,
        )
        conn.commit()


# Testing purpose
def search_institution_by_prefix(prefix: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT Name FROM Institution WHERE Name LIKE ?;"
        cursor.execute(query, (prefix + '%',))
        results = cursor.fetchall()
        return [row[0] for row in results] 