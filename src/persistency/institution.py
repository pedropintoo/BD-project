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
            None,
            )

class InstitutionSimple(NamedTuple):
    InstitutionID: str
    Name: str
    Address: str

class InstitutionDetails(NamedTuple):
    InstitutionID: str
    Name: str
    Address: str
    AuthorsCount: int
    AuthorsList: list[str]  # Adiciona uma lista para os títulos dos artigos

def read(institution_id: str) -> InstitutionDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC ListAllInstitutionsDetails @InstitutionID = ?", institution_id)
        # Primeiro conjunto de resultados: Detalhes da Institution
        institution_row = cursor.fetchone()

        if institution_row:
            institution_details = InstitutionDetails(
                institution_row[0] or None,
                institution_row[1] or None,
                institution_row[2] or None,
                institution_row[3] or None,
                []

            )

            # Segundo conjunto de resultados: Lista de Artigos
            cursor.nextset()  # Move para o próximo conjunto de resultados
            authors = cursor.fetchall()
            authors_list = [author[0] for author in authors]

            # Atualiza author_details com a lista de artigos
            institution_details = institution_details._replace(AuthorsList=authors_list)

            return institution_details
        else:
            return InstitutionDetails(
                None,
                None,
                None,
                0,
                []

            )

def create(institution: Institution):
    with create_connection() as conn:
        print("Institution: ", institution)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Institution (InstitutionID, Name, Address, AuthorsCount)
            VALUES (?, ?, ?, ?);
            """,
            (institution.InstitutionID, institution.Name, institution.Address, institution.AuthorsCount)
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


def update(institution_id: str, institution: Institution):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            
            # Atualiza os detalhes da instituição
            cursor.execute(
                """
                UPDATE Institution
                SET Name = ?, Address = ?
                WHERE InstitutionID = ?;
                """,
                institution.Name if institution.Name != "None" else None,
                institution.Address if institution.Address != "None" else None,
                institution_id
            )
            conn.commit()
        except IntegrityError as ex:
            if ex.args[0] == "23000":
                raise Exception(f"Institution {institution_id} cannot be deleted.") from ex

# Testing purpose
def search_institution_by_prefix(prefix: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT Name FROM Institution WHERE Name LIKE ?;"
        cursor.execute(query, (prefix + '%',))
        results = cursor.fetchall()
        return [row[0] for row in results] 