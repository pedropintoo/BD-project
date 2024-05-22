import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Journal


class JournalSimple(NamedTuple):
    JournalID: str
    Name: str
    PrintISSN: str
    Url: str

class JournalForm(NamedTuple):
    Name: str
    PrintISSN: str
    EletronicISSN: str
    Url: str
    Publisher: str

class JournalDetails(NamedTuple):
    Name: str
    PrintISSN: str
    EletronicISSN: str
    Url: str
    Publisher: str
    ArticlesCount: int
    VolumesCount: int
    VolumesList: dict[str, list[str]] # dict of volume number and list of articles

NOT_FOUND = JournalSimple(
            None,
            None,
            None,
            None
            )


def read(journal_id: str) -> JournalDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC ListJournalDetails @JournalID = ?", journal_id)
        
        journal_row = cursor.fetchone()
        journal_details = JournalDetails(
            journal_row[0] or "",
            journal_row[1] or "",
            journal_row[2] or "",
            journal_row[3] or "",
            journal_row[4] or "",
            journal_row[5] or 0,
            0,
            {}  # start empty
        )

        # copy the journal details to a new variable
        cursor.nextset()
        volumes = cursor.fetchall()
        volumes_dict = {}
        for volume in volumes:
            volume_number = volume[0]
            article_list = volume[1]
            volumes_dict[volume_number] = article_list

        journal_details = journal_details._replace(VolumesList=volumes_dict)

        return journal_details    


def create(journal_id, journal):
    with create_connection() as conn:
        cursor = conn.cursor()
        print("Try to create journal")

        cursor.execute("EXEC CreateJournal @JournalID = ?, @Name = ?, @PrintISSN = ?, @EletronicISSN = ?, @Url = ?, @Publisher = ?;",
                          journal_id, journal.Name, journal.PrintISSN, journal.EletronicISSN, journal.Url, journal.Publisher
        )

        conn.commit()

def list_all_by_volume_count():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByArticlesCount;")
        rows = cursor.fetchall()
        return [JournalSimple(
            row.JournalID or "Not found",
            row.Name or "Not found",
            row.PrintISSN or "Not found",
            row.Url or "Not found"
        ) for row in rows]
    
def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByJournalName;")
        rows = cursor.fetchall()
        return [JournalSimple(
            row.JournalID or "Not found",
            row.Name or "Not found",
            row.PrintISSN or "Not found",
            row.Url or "Not found"
        ) for row in rows]

def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderBySearchJournalName @Name = ?", name)
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [JournalSimple(
            row.JournalID or "Not found",
            row.Name or "Not found",
            row.PrintISSN or "Not found",
            row.EletronicISSN or "Not found",
            row.Url or "Not found",
            row.Publisher or "Not found"
        ) for row in rows]


def delete(journal_id: str):    
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC DeleteJournal @JournalID = ?", journal_id)
            conn.commit()
        except Exception as e:
            print("Error: ", e)
            raise

def generate_journal_id(name: str, print_issn: str, eletronic_issn: str, url: str, publisher: str) -> str:
    combined = f"{name}{print_issn}{eletronic_issn}{url}{publisher}"
    # Generate SHA-256 hash of the combined string
    hash_object = hashlib.sha256(combined.encode())
    # Get the first 36 characters of the hex digest
    journal_id = hash_object.hexdigest()[:36]
    return journal_id
       
def update(journal_id: str, journal: Journal):
    with create_connection() as conn:
        cursor = conn.cursor()
       
        cursor.execute(
            """
            EXEC UpdateJournal
            @JournalID = ?, @Name = ?, @PrintISSN = ?, @EletronicISSN = ?, @Url = ?, @Publisher = ?;
            """,
            journal_id,
            journal.Name if journal.Name != "" else None,
            journal.PrintISSN if journal.PrintISSN != "" else None,
            journal.EletronicISSN if journal.EletronicISSN != "" else None,
            journal.Url if journal.Url != "" else None,
            journal.Publisher if journal.Publisher != "" else None
        )
        conn.commit()