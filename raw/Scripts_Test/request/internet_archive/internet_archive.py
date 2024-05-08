import pyodbc
from scholarly import scholarly
import requests
import json
import os

ARTICLE_ID = 0
JOURNAL_ID = 0
AUTHOR_ID = 0
INSTITUTION_ID = 0

def getArticleID():
    global ARTICLE_ID
    ARTICLE_ID = ARTICLE_ID + 1
    return ARTICLE_ID

def getJournalID():
    global JOURNAL_ID
    JOURNAL_ID = JOURNAL_ID + 1
    return JOURNAL_ID

def getAuthorID():
    global AUTHOR_ID
    AUTHOR_ID = AUTHOR_ID + 1
    return AUTHOR_ID    

def getInstitutionID():
    global INSTITUTION_ID
    INSTITUTION_ID = INSTITUTION_ID + 1
    return INSTITUTION_ID    

def insert_database(journal, journalVolume, article, institutions, authors):

    # Parameters
    server = r'tcp:mednat.ieeta.pt\SQLSERVER,8101'
    database = 'p5g1'
    username = 'p5g1'
    password = os.getenv("SQL_PASSWORD")
    cnxn_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Connection
    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()

    # Data to INSERT
    dados_a_inserir = institutions

    # Preparar e executar a instrução SQL de inserção
    instrucao_sql = 'INSERT INTO Institution VALUES (?, ?, ?)'
    for dado in dados_a_inserir:
        cursor.execute(instrucao_sql, dado)

    # Commitar as inserções e fechar a conexão
    cnxn.commit()
    cursor.close()
    cnxn.close()

    print("Dados inseridos com sucesso.")


def main():

    h = {'Accept': 'application/json'}
    p = {
        'q': '*',

        'title': '*',
        'abstracts': '*',
        'doi': '*',
        'pages': '*',
        'journal': '*',

        'author': '*',
        
        'volume': '*',
        
        'year': '*',
        
        

        'limit': 10, # max 100  
        'offset': 0,  
        'filter_type': 'papers',  
        'filter_availability': 'oa',
        'sort_order': 'relevancy',
        'filter_time': 'all_time'
    }

    response = requests.get("https://scholar.archive.org/search", headers=h, params=p)

    if response.status_code == 200:
        data = response.json()
        
        for result in data['results']:
            biblio = result['biblio']
            
            title = biblio.get('title', "NULL")
            #print(f"Title: {title}")

            DOI = biblio.get('doi', "NULL")
            #print(f"DOI: {DOI}")  

            pages = biblio.get('pages', "NULL")
            StartPage = pages
            EndPage = pages
            if (pages != "NULL"):
                if "-" in pages:
                    StartPage = pages.split("-")[0]
                    EndPage = pages.split("-")[1]

            #print(f"First Page: {StartPage}")
            #print(f"Last Page: {EndPage}")

            release_date = biblio.get('release_date', "NULL")
            #print(f"Release Date: {release_date}")

            # contrib_names = biblio.get('contrib_names', "NULL")
            # print(f"Authors: {contrib_names}")

            container_name = biblio.get('container_name', "NULL")
            #print(f"Journal: {container_name}")

            container_ident = biblio.get('container_ident', "NULL")
            #print(f"Journal Identifier: {container_ident}")

            container_issn = biblio.get('container_issnl', "NULL")
            #print(f"Journal ISSN: {container_issn}")

            # container_type = biblio.get('container_type', "NULL")
            # print(f"Journal Type: {container_type}")

            volume = biblio.get('volume', "NULL")
            #print(f"Volume: {volume}")

            publisher = biblio.get('publisher', "NULL")
            #print(f"Publisher: {publisher}")

            abstracts = result['abstracts']
            abstract = "NULL"
            if abstracts:
                abstract = abstracts[0]['body']
            #print(f"Abstract: {abstract}")

            ## scholarly

            search_query = scholarly.search_single_pub(title)
            bib = search_query.get('bib', "NULL")

            authors_name = bib.get('author', "NULL")
            print(authors_name)
            if authors_name != "NULL":
                scholar_id = search_query.get('author_id', "NULL")
                for i in range(len(scholar_id)):
                    if scholar_id[i] == '':
                        scholar_id[i] = "NULL"
                institutions = []
                authors = []
                for i in range(len(authors_name)):
                    institution_name = "NULL"
                    email_domain = "NULL"
                    inst_id = "NULL"

                    if scholar_id and scholar_id[i]:
                        print(f"Scholar ID: {scholar_id[i]}")
                        if scholar_id[i] != "NULL":
                            author_info = scholarly.search_author_id(scholar_id[i])
                            
                            institution_name = author_info.get("affiliation","NULL")
                            print(f"Institution: {institution_name}")

                            email_domain = author_info.get("email_domain","NULL")
                            print(f"Email_domain: {email_domain}")

                    if institution_name != "NULL":
                        #
                        institutions.append((getInstitutionID(), institution_name, "NULL"))

                        inst_id = INSTITUTION_ID

                    #
                    authors.append((getAuthorID(), authors_name[i], email_domain, scholar_id[i], inst_id))
                            
            #
            journal = (getJournalID(), container_name, "NULL", container_issn, "NULL", publisher)
            
            #
            journalVolume = (journal[0], volume, release_date)
            
            #
            article = (getArticleID(), title, abstract, DOI, StartPage, EndPage, journal[0], volume)
            
            print("Journal:", journal)
            print("JournalVolume:", journalVolume)
            print("Article:", article) 
            for institution in institutions:
                print("Institution:",institution)
            for author in authors:
                print("Author:",author)

            insert_database(journal, journalVolume, article, institutions, authors)    

            print("-"*10)    

    else:
        print(f'Failed to fetch data: {response.status_code}')



if __name__ == "__main__":
    main()        