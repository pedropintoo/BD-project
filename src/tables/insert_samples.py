import sys
sys.path.append('.')
 
import pyodbc
import json
import urllib
import gzip
from persistency.session import create_connection
from tables import *
from full_data.download import get_fullData_links


def insert_author(author: Author):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Author VALUES (?, ?, ?, ?, ?)",
                author.AuthorID,
                author.Name,
                author.Url,
                author.ORCID,
                author.InstitutionID)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            print("Author integrity error.", e)
        except pyodbc.ProgrammingError as e:
            print("Author creation error.", e) 
        except pyodbc.DataError as e:
            print("Truncated maybe. Error...", author, e)  
        except Exception as e:
            print("Error...", author, e)

def insert_institution(institution: Institution):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Institution VALUES (?, ?, ?)",
                institution.InstitutionID,
                institution.Name,
                institution.Address)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            print("Institution integrity error.", e)
        except pyodbc.ProgrammingError as e:
            print("Institution creation error.", e)
        except pyodbc.DataError as e:
            print("Truncated maybe. Error...", Institution, e) 
        except Exception as e:
            print("Error...", Institution, e)   
             

def insert_authors_and_institutions(buffer):
    # Read data from the file into a list of dictionaries
    for line in buffer:
        # Load each line as JSON
        author_data = json.loads(line)
        institution_name = author_data['affiliations'][0] if author_data["affiliations"] else None

        if institution_name:
            # Create Institution object
            institution = Institution(
                InstitutionID = abs(hash(institution_name)) % (10 ** 10),
                Name = institution_name,
                Address = None
                )

            # Insert institution data
            insert_institution(institution)


        # Create Author object
        author = Author(
            AuthorID = author_data["authorid"],
            Name = author_data["name"],
            Url = author_data["url"],
            ORCID = author_data["externalids"].get("ORCID", None) if author_data["externalids"] else None,
            InstitutionID = institution.InstitutionID if institution_name else None
            )

        # Insert author data
        insert_author(author)

def insert_article(article: Article):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Article VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                article.ArticleID,
                article.Title,
                article.Abstract,
                article.DOI,
                article.StartPage,
                article.EndPage,
                article.JournalID,
                article.Volume)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            print("Article integrity error.", e)
        except pyodbc.ProgrammingError as e:
            print("Article creation error.", e)
        except pyodbc.DataError as e:
            print("Truncated maybe. Error...", article, e) 
        except Exception as e:
            print("Error...", article, e)

def insert_topic(topic: Topic):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
                "SELECT * FROM Topic WHERE TopicID=?",
                topic.TopicID
                )
        result = cursor.fetchone()
        if result is None:
            return

        try:
            cursor.execute(
                "INSERT INTO Topic VALUES (?, ?, ?)",
                topic.TopicID,
                topic.Name,
                topic.Description)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            print("Topic integrity error.", e)
        except pyodbc.ProgrammingError as e:
            print("Topic creation error.", e)
        except pyodbc.DataError as e:
            print("Truncated maybe. Error...", topic, e) 
        except Exception as e:
            print("Error...", topic, e)

def insert_journal(journal: Journal):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
                "SELECT * FROM Journal WHERE JournalID=?",
                journal.JournalID
                )
        result = cursor.fetchone()
        if result is None:
            return

        try:
            cursor.execute(
                "INSERT INTO Journal VALUES (?, ?, ?, ?, ?, ?)",
                journal.JournalID,
                journal.Name,
                journal.PrintISSN,
                journal.EletronicISSN,
                journal.Frequency,
                journal.Publisher)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            print("Journal integrity error.", e)
        except pyodbc.ProgrammingError as e:
            print("Journal creation error.", e)
        except pyodbc.DataError as e:
            print("Truncated maybe. Error...", journal, e) 
        except Exception as e:
            print("Error...", journal, e)

def insert_journalVolume(journalVolume: JournalVolume):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO JournalVolume VALUES (?, ?, ?)",
                journalVolume.JournalID,
                journalVolume.Volume,
                journalVolume.PublicationDate)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            print("JournalVolume integrity error.", e)
        except pyodbc.ProgrammingError as e:
            print("JournalVolume creation error.", e)
        except pyodbc.DataError as e:
            print("Truncated maybe. Error...", journalVolume, e) 
        except Exception as e:
            print("Error...", journalVolume, e)


def insert_articles_and_topics_and_journals(buffer):
    # Read data from the file into a list of dictionaries
    for line in buffer:
        # Load each line as JSON
        article_data = json.loads(line)
        
        if article_data["s2fieldsofstudy"] is None:
            continue

        # Get topics
        for item in article_data["s2fieldsofstudy"]:
            topic_name = item["category"]    
            # Create Topic object
            topic = Topic(
                TopicID = str(abs(hash(topic_name)) % (10 ** 10)),
                Name = topic_name,
                Description = None
            )

            # Insert topic data
            insert_topic(topic)

        journal_info = article_data["journal"]
        if journal_info == "" or journal_info is None:
            continue

        startPage = endPage = 0
        pages = journal_info["pages"]
        if pages is not None:
            pages = pages.replace('\n', '').replace('\\n', '').strip()
        volume = journal_info.get("volume")
        if volume is None:
            volume = -1
        journalName = journal_info["name"]

        journalID = str(abs(hash(journalName)) % (10 ** 10))
        # create journal object
        journal = Journal(
            JournalID = journalID,
            Name = journalName,
            PrintISSN = None,
            EletronicISSN = None,
            Frequency = None,
            Publisher = None
        )
        insert_journal(journal)

        # create journal volume object
        journalVolume = JournalVolume(
            JournalID = journalID,
            Volume = volume,
            PublicationDate = None,
        )
        insert_journalVolume(journalVolume)
        
        # Check if the data format is correct
        if pages and isinstance(pages, str) and '-' in pages:
            # Clean up whitespace and line breaks
            pages = pages.strip()
            
            # Check if the format is 'Number1-Number2' after cleaning
            if pages.count('-') == 1 and all(part.isdigit() for part in pages.split('-')):
                startPage, endPage = map(int, pages.split('-'))
    
        if volume and isinstance(volume, str) and volume.isdigit():
            volume = int(volume)
        else:
            volume = 0
        
        # Create Article object
        article = Article(
            ArticleID = article_data["corpusid"],
            Title = article_data["title"],
            Abstract = None,
            DOI = article_data["externalids"].get("DOI", None) if article_data["externalids"] else None,
            StartPage = startPage,
            EndPage = endPage,
            JournalID = journalID,
            Volume = volume
            )

        # Insert article data
        insert_article(article)


if __name__ == '__main__':
    # Authors + Institutions
    file_path = "tables\\sample-data\\authors\\authors-sample.jsonl"
    buffer = open(file_path, "r", encoding="utf-8").readlines()
    insert_authors_and_institutions(buffer)

    # Articles + Topics + Journals
    file_path1 = "tables\\sample-data\\papers\\papers-sample.jsonl"
    buffer1 = open(file_path1, "r", encoding="utf-8").readlines()
    # miss file publication-venues
    insert_articles_and_topics_and_journals(buffer1)

    # buffer = gzip.open("tables\\full_data\\author0.jsonl.gz", "r").readlines()
    # print("buffer length: ", len(buffer))
    # for i in range(0, len(buffer), 100):
    #     insert_authors_and_institutions(buffer[i:i+100])
    #     print("inserted [", i, ":", i+100, "].")

    # buffer = open(file_path, "r", encoding="utf-8").readlines()
    # insert_authors_and_institutions(buffer)