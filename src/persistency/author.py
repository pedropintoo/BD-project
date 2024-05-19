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
    InstitutionName: str
    ArticlesCount: int
    ArticlesList: list[str]  # Adiciona uma lista para os títulos dos artigos

class AuthorUpdate(NamedTuple):
    AuthorID: str
    Name: str
    Url: str
    ORCID: str
    InstitutionID: str
    InstitutionName: str

    

def read(author_id: str) -> AuthorDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC ListAllAuthorsDetails @AuthorID = ?", author_id)

        # Primeiro conjunto de resultados: Detalhes do Autor
        author_row = cursor.fetchone()
        if author_row:
            author_details = AuthorDetails(
                author_row[0] or None,
                author_row[1] or None,
                author_row[2] or None,
                author_row[3] or None,
                author_row[4] or None,
                author_row[5] or None,
                author_row[6] or 0,
                []  # Inicializa uma lista vazia para os artigos
            )

            # Segundo conjunto de resultados: Lista de Artigos
            cursor.nextset()  # Move para o próximo conjunto de resultados
            articles = cursor.fetchall()
            articles_list = [article[0] for article in articles]

            # Atualiza author_details com a lista de artigos
            author_details = author_details._replace(ArticlesList=articles_list)

            return author_details
        else:
            return AuthorDetails(
                None,
                None,
                None,
                None,
                None,
                None,
                0,
                []
            )


def create(author: Author):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Author (AuthorID, Name, Url, ORCID, InstitutionID, ArticlesCount)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (author.AuthorID, author.Name, author.Url, author.ORCID, author.InstitutionID, author.ArticlesCount)
        )
        conn.commit()

def list_all_by_article_count():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByArticlesCount;")
        rows = cursor.fetchall()
        return [AuthorSimple(
            row.AuthorID or None,
            row.Name or None,
            row.Url or None,
            row.InstitutionName or None
        ) for row in rows]

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByAuthorName;")
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
        cursor.execute("EXEC OrderBySearchAuthorName @AuthorName = ?", name)
        rows = cursor.fetchall()
        
        if rows == None:
            return NOT_FOUND

        return [AuthorSimple(
            row.AuthorID or None,
            row.Name or None,
            row.Url or None,
            row.InstitutionName or None
        ) for row in rows]
    
def delete(author_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC DeleteAuthor @AuthorID = ?", author_id)
            cursor.commit()
        except Exception as e:
            print("Error:", e)
            raise


def get_institution_id(institution_name: str) -> str:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC GetInstitutionIDByName @InstitutionName = ?", institution_name)
        row = cursor.fetchone()
        print("Institution ID")
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
