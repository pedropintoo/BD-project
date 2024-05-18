import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Author

NOT_FOUND = Author(
            None,
            None,
            None,
            None,
            None
            )

class AuthorSimple(NamedTuple):
    AuthorID: str
    Name: str
    Url: str
    InstitutionName: str = None

class AuthorDetails(NamedTuple):
    AuthorID: str
    Name: str
    Url: str
    ORCID: str
    InstitutionID: str
    InstitutionName: str = None    

    

def read(author_id: str) -> Author:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC ListAllAuthorsDetails @AuthorID = ?", author_id)
        row = cursor.fetchone()
        if row:
            return AuthorDetails(
                row[0] or None,
                row[1] or None,
                row[2] or None,
                row[3] or None,
                row[4] or None,
                row[5] or None
            )
        else:
            return AuthorDetails(
                None,
                None,
                None,
                None,
                None,
                None
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
        cursor.execute("EXEC ListAllAuthors;")
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
        cursor.execute("SELECT * FROM Author WHERE Name LIKE ?;", '%'+name+'%')
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [Author(
            row.AuthorID or None,
            row.Name or None,
            row.Url or None,
            row.ORCID or None,
            row.InstitutionID or None,
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


def get_institution_id(institution_name: str) -> str:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC GetInstitutionIDByName @InstitutionName = ?", institution_name)
        row = cursor.fetchone()
        print("Institution ID")
        print(row)
        if row:
            return row[0]
        return None

def generate_author_id(name: str, institution_id: str) -> str:
    # Combine name and institution_id
    combined = f"{name}{institution_id}"
    # Generate SHA-256 hash of the combined string
    hash_object = hashlib.sha256(combined.encode())
    # Get the first 10 characters of the hex digest
    author_id = hash_object.hexdigest()[:10]
    return author_id

                
def update(author_id: str, author: Author):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            
            # Atualiza os detalhes do autor
            cursor.execute(
                """
                UPDATE Author
                SET Name = ?, Url = ?, ORCID = ?, 
                    InstitutionID = ?
                WHERE AuthorID = ?;
                """,
                author.Name if author.Name != "None" else None,
                author.Url if author.Url != "None" else None,
                author.ORCID if author.ORCID != "None" else None,
                author.InstitutionID if author.InstitutionID != "None" else None,
                author_id
            )
            conn.commit()
        except IntegrityError as ex:
            if ex.args[0] == "23000":
                raise Exception(f"Author {author_id} cannot be deleted.") from ex
