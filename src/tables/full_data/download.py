import sys
sys.path.append('.')

from semanticscholar import SemanticScholar
import requests
import os
import urllib
import gzip
import pyodbc
import json
from persistency.session import create_connection
from tables.tables import *

api_key = os.getenv('API_KEY_SEMANTICSCHOLAR')  # API key
sch = SemanticScholar(api_key=api_key)


def insert_belongs_to_many(belongs_to):
    with create_connection() as conn:
        cursor = conn.cursor()

        query = "INSERT INTO Belongs_to VALUES (?, ?)"

        try:
            cursor.executemany(query, belongs_to)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            for belongs_to in belongs_to:
                try:
                    cursor.execute(query, belongs_to)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("belongs_to integrity error.", belongs_to, e)
                except pyodbc.ProgrammingError as e:
                    print("belongs_to creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", belongs_to, e) 
                except Exception as e:
                    print("Error...", belongs_to, e)
        except pyodbc.ProgrammingError as e:
            print("belongs_to creation error.", e)
        except pyodbc.DataError as e:
            # try to insert separately
            for belongs_to in belongs_to:
                try:
                    cursor.execute(query, belongs_to)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("belongs_to integrity error.", belongs_to, e)
                except pyodbc.ProgrammingError as e:
                    print("belongs_to creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", belongs_to, e) 
                except Exception as e:
                    print("Error...", belongs_to, e)

        except Exception as e:
            print("Error...", e)


def insert_wrote_by_many(wrote_by):
    with create_connection() as conn:
        cursor = conn.cursor()

        query = "INSERT INTO Wrote_by VALUES (?, ?)"

        try:
            cursor.executemany(query, wrote_by)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            for wrote_by in wrote_by:
                try:
                    cursor.execute(query, wrote_by)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("wrote_by integrity error.", wrote_by, e)
                except pyodbc.ProgrammingError as e:
                    print("wrote_by creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", wrote_by, e) 
                except Exception as e:
                    print("Error...", wrote_by, e)
        except pyodbc.ProgrammingError as e:
            print("wrote_by creation error.", e)
        except pyodbc.DataError as e:
            # try to insert separately
            for wrote_by in wrote_by:
                try:
                    cursor.execute(query, wrote_by)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("wrote_by integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("wrote_by creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", wrote_by, e) 
                except Exception as e:
                    print("Error...", wrote_by, e)

        except Exception as e:
            print("Error...", e)


def insert_author_many(authors):
    with create_connection() as conn:
        cursor = conn.cursor()

        query = "INSERT INTO Author VALUES (?, ?, ?, ?, ?, ?)"

        try:
            cursor.executemany(query, authors)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            for author in authors:
                try:
                    cursor.execute(query, author)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("Author integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("Author creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", author, e)  
                except Exception as e:
                    print("Error...", author, e)
        except pyodbc.ProgrammingError as e:
            print("Author creation error.", e) 
        except pyodbc.DataError as e:
            for author in authors:
                try:
                    cursor.execute(query, author)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("Author integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("Author creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", author, e) 
                except Exception as e:
                    print("Error...", author, e)
        except Exception as e:
            print("Error...", authors, e)

def insert_institution_many(institutions):
    with create_connection() as conn:
        cursor = conn.cursor()

        query = "INSERT INTO Institution VALUES (?, ?, ?, ?)"

        try:
            cursor.executemany(query, institutions)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            for institution in institutions:
                try:
                    cursor.execute(query, institution)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("Institution integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("Institution creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", institution, e) 
                except Exception as e:
                    print("Error...", institution, e)
        except pyodbc.ProgrammingError as e:
            print("Institution creation error.", e)
        except pyodbc.DataError as e:
            for institution in institutions:
                try:
                    cursor.execute(query, institution)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("Institution integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("Institution creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", institution, e) 
                except Exception as e:
                    print("Error...", institution, e)
        except Exception as e:
            print("Error...", Institution, e)   

def insert_journal_many(journals):
    with create_connection() as conn:
        cursor = conn.cursor()

        query = "INSERT INTO Journal VALUES (?, ?, ?, ?, ?, ?, ?)"
        
        try:
            cursor.executemany(query, journals)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            for journal in journals:
                try:
                    cursor.execute(query, journal)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("Journal integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("Journal creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", journal, e)
                except Exception as e:
                    print("Error...", journal, e)
        except pyodbc.ProgrammingError as e:
            print("Journal creation error.", e)
        except pyodbc.DataError as e:
            # try to insert separately
            for journal in journals:
                try:
                    cursor.execute(query, journal)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("Journal integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("Journal creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", journal, e) 
                except Exception as e:
                    print("Error...", journal, e)     
        except Exception as e:
            print("Error...", e)


def insert_article_many(articles):
    with create_connection() as conn:
        cursor = conn.cursor()

        query = "INSERT INTO Article VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

        try:
            cursor.executemany(query, articles)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            for article in articles:
                try:
                    cursor.execute(query, article)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("Article integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("Article creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", article, e)
                except Exception as e:
                    print("Error...", article, e)
        except pyodbc.ProgrammingError as e:
            print("Article creation error.", e)
        except pyodbc.DataError as e:
            # try to insert separately
            for article in articles:
                try:
                    cursor.execute(query, article)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("Article integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("Article creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", article, e) 
                except Exception as e:
                    print("Error...", article, e)
        except Exception as e:
            print("Error...", article, e)

def insert_journalVolume_many(journalVolumes):
    with create_connection() as conn:
        cursor = conn.cursor()

        query = "INSERT INTO JournalVolume VALUES (?, ?, ?)"

        try:
            cursor.executemany(query, journalVolumes)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            for journalVolume in journalVolumes:
                try:
                    cursor.execute(query, journalVolume)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("JournalVolume integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("JournalVolume creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", journalVolume, e) 
                except Exception as e:
                    print("Error...", journalVolume, e)
        except pyodbc.ProgrammingError as e:
            print("JournalVolume creation error.", e)
        except pyodbc.DataError as e:
            for journalVolume in journalVolumes:
                try:
                    cursor.execute(query, journalVolume)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    print("JournalVolume integrity error.", e)
                except pyodbc.ProgrammingError as e:
                    print("JournalVolume creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", journalVolume, e) 
                except Exception as e:
                    print("Error...", journalVolume, e)
        except Exception as e:
            print("Error...", journalVolume, e)

def insert_topic_many(topics):
    with create_connection() as conn:
        cursor = conn.cursor()
        
        query = "INSERT INTO Topic VALUES (?, ?, ?, ?)"

        try:
            cursor.executemany(query, topics)
            cursor.commit()
        except pyodbc.IntegrityError as e:
            for topic in topics:
                try:
                    cursor.execute(query, topic)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    #print("Topic integrity error.", e)
                    pass
                except pyodbc.ProgrammingError as e:
                    print("Topic creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", e) 
                except Exception as e:
                    print("Error...", topic, e)
        except pyodbc.ProgrammingError as e:
            print("Topic creation error.", e)
        except pyodbc.DataError as e:
            for topic in topics:
                try:
                    cursor.execute(query, topic)
                    conn.commit()
                except pyodbc.IntegrityError as e:
                    #print("Topic integrity error.", e)
                    pass
                except pyodbc.ProgrammingError as e:
                    print("Topic creation error.", e)
                except pyodbc.DataError as e:
                    print("Truncated maybe. Error...", e) 
                except Exception as e:
                    print("Error...", topic, e)
        except Exception as e:
            print("Error...", topics, e)


############################################################################################################

def insert_journals(buffer):
    journals = []
    # Read data from the file into a list of dictionaries
    for line in buffer:
        # Load each line as JSON
        journal_data = json.loads(line)
        
        journal_name = journal_data["name"]
        
        if journal_data["id"] == 0:
            continue

        # Create Journal object
        journal = Journal(
            JournalID = journal_data["id"],
            Name = journal_name,
            PrintISSN = journal_data["issn"],
            EletronicISSN = journal_data["alternate_issns"][0] if journal_data["alternate_issns"] else None,
            Url = journal_data["url"],
            Publisher = None,
            ArticlesCount = 0
            )

        journals.append(journal)

    # Insert journal data
    insert_journal_many(journals)

def insert_authors_and_institutions(buffer):
    institutions = []
    buffer_articles = []
    authors = []
    wrote_by = []
    
    # Read data from the file into a list of dictionaries
    for line in buffer:
        # Load each line as JSON
        author_data = json.loads(line)
        institution_name = author_data['affiliations'][0] if author_data["affiliations"] else None

        if institution_name is None:
            continue

        # Create Institution object
        institution = Institution(
            InstitutionID = abs(hash(institution_name)) % (10 ** 10),
            Name = institution_name,
            Address = None,
            AuthorsCount = 0
            )

        institutions.append(institution)
        

        # Create Author object
        author = Author(
            AuthorID = author_data["authorid"],
            Name = author_data["name"],
            Url = author_data["url"],
            ORCID = author_data["externalids"].get("ORCID")[0] if (author_data["externalids"] and author_data["externalids"].get("ORCID") != None) else None,
            InstitutionID = institution.InstitutionID if institution_name else None,
            ArticlesCount = 0
            )

        authors.append(author)

        raw = sch.get_author(author_data["authorid"]).papers
        if len(raw) > 0:
            print(len(raw))
            buffer_articles.append(raw)
            for article in raw:
                wrote_by.append((str(article["externalIds"].get("CorpusId", None)), author_data["authorid"]))

    if len(institutions) == 0:
        return

    # Insert institution data
    insert_institution_many(institutions)

    # Insert paper data
    if len(buffer_articles) > 0:
        # TODO: return authors and wrote_by!!!
        insert_articles_and_topics_and_journalVersions(buffer_articles[0])

    # Insert author data
    insert_author_many(authors)

    # Insert wrote_by data
    insert_wrote_by_many(wrote_by)  # may insert articles that are not in the table


def insert_articles_and_topics_and_journalVersions(buffer):
    articles = []
    journals = []
    topics = []
    journalVolumes = []
    belongs_to = [] 
    # Read data from the file into a list of dictionaries
    for article_data in buffer:
        
        # We only insert papers who has a topic
        if article_data["s2FieldsOfStudy"] is None or article_data["externalIds"].get("CorpusId", None) is None:
            continue
        
        article_topics = []

        # Get topics
        for item in article_data["s2FieldsOfStudy"]:
            topic_name = item["category"]    
            # Create Topic object
            topic = Topic(
                TopicID = str(abs(hash(topic_name)) % (10 ** 10)),
                Name = topic_name,
                Description = None,
                ArticlesCount = 0
            )

            if topic.TopicID in article_topics:
                continue

            article_topics.append(topic.TopicID)
            topics.append(topic)

        print(article_data) 

        journal_info = article_data["journal"]
        if journal_info == "" or journal_info is None:
            continue

        startPage = endPage = 0
        pages = journal_info.get("pages")
        if pages is not None:
            pages = pages.replace('\n', '').replace('\\n', '').strip()
        volume = journal_info.get("volume")
        if volume is None:
            continue
        journalName = journal_info.get("name")
        
        journalID = str(abs(hash(journalName)) % (10 ** 40))
        
        if journalID == "0" or journalName is None or journalName == "":
            continue

        # create journal object
        journal = Journal(
            JournalID = journalID,
            Name = journalName,
            PrintISSN = None,
            EletronicISSN = None,
            Url = None,
            Publisher = None,
            ArticlesCount = 0
        )

        journals.append(journal)
        
        if article_data["publicationDate"] is None or article_data["publicationDate"] == "":
            continue

        print( article_data)
        # create journal volume object
        journalVolume = JournalVolume(
            JournalID = journalID,
            Volume = volume,
            PublicationDate = article_data["publicationDate"],
        )
        
        journalVolumes.append(journalVolume)
        
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
            ArticleID = str(article_data["externalIds"]["CorpusId"]),
            Title = article_data["title"],
            Abstract = article_data["abstract"] if article_data["abstract"] else None,
            DOI = article_data["externalIds"].get("DOI", None) if article_data["externalIds"] else None,
            StartPage = startPage,
            EndPage = endPage,
            JournalID = journalID,
            Volume = volume,
            AuthorsCount = 0
            )

        articles.append(article)   

        for topicID in article_topics:
            belongs_to.append((topicID, article.ArticleID))
        

    # Insert topic data
    insert_topic_many(topics)

    # Insert journal data
    insert_journal_many(journals)

    # Insert journalVolume data
    insert_journalVolume_many(journalVolumes)

    # Insert article data
    insert_article_many(articles)

    # Insert belongs_to data
    insert_belongs_to_many(belongs_to)


############################################################################################################

def get_fullData_links(dataset, release = "latest"):
    # Define the API endpoint URL
    url = f'https://api.semanticscholar.org/datasets/v1/release/{release}/dataset/{dataset}'

    api_key = os.getenv('API_KEY_SEMANTICSCHOLAR')  # API key

    # Define headers with API key
    headers = {'x-api-key': api_key}

    # Send the API request
    response = requests.get(url, headers=headers)
    links = None

    # Check response status
    if response.status_code == 200:
        response_data = response.json()
        # Process and print the response data as needed
        
        links = response_data['files']
        
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

    return links

if __name__ == '__main__':
    # Download the data from the API
    # link = get_fullData_links("publication-venues","2024-04-02")[0]
    # urllib.request.urlretrieve(link, "tables\\full_data\\publication-venues\\publication-venues0.jsonl.gz")
    #link = get_fullData_links("authors","2024-04-02")[0]
    #urllib.request.urlretrieve(link, "tables\\full_data\\authors\\authors0.jsonl.gz")

    # Use some data from the downloaded files

    # buffer = gzip.open("tables\\full_data\\publication-venues\\publication-venues0.jsonl.gz", "r").readlines()
    # print("buffer length: ", len(buffer))
    # inc = 25
    # max = 600
    # for i in range(0, max, inc):
    #     insert_journals(buffer[i:i+inc])
    #     print("inserted [", i, ":", i+inc, "].")
    
    buffer = gzip.open("tables\\full_data\\authors\\authors0.jsonl.gz", "r").readlines()
    print("buffer length: ", len(buffer))
    inc = 100
    max = 200000
    for i in range(0, max, inc):
        insert_authors_and_institutions(buffer[i:i+inc])
        print("inserted [", i, ":", i+inc, "].")

    