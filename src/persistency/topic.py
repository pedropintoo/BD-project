import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection
from tables.tables import Topic

class TopicSimple(NamedTuple):
    TopicID: str
    Name: str
    Description: str

class TopicForm(NamedTuple):
    Name: str
    Description: str

class TopicDetails(NamedTuple):
    Name: str
    Description: str
    ArticlesCount: int
    ArticlesList: list[str]    

NOT_FOUND = TopicSimple(
            None,
            None,
            None
            )

def read(topic_id: str) -> TopicDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC ListTopicDetails @TopicID = ?", topic_id)

        topic_row = cursor.fetchone()
        topic_details = TopicDetails(
            topic_row[0] or "",
            topic_row[1] or "",
            topic_row[2] or 0,
            []  # start empty
        )

        # copy the author details to a new variable
        cursor.nextset()
        articles = cursor.fetchall()
        articles_list = [article[0] for article in articles]
        topic_details = topic_details._replace(ArticlesList=articles_list)

        return topic_details


def create(topic_id, topic):
    with create_connection() as conn:
        cursor = conn.cursor()
        print("Try to create topic")

        cursor.execute(
            "EXEC CreateTopic @TopicID = ?, @Name = ?, @Description = ?",
            topic_id, topic.Name, topic.Description
        )

        conn.commit()


def list_all_by_article_count():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByArticlesCount;")
        rows = cursor.fetchall()

        return [TopicSimple(
            row.TopicID or None,
            row.Name or None,
            row.Description or None
        ) for row in rows]

def list_all():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderByTopicName;")
        rows = cursor.fetchall()

        return [TopicSimple(
            row.TopicID or None,
            row.Name or None,
            row.Description or None
        ) for row in rows]
       
def filterByName(name: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC OrderBySearchTopicName @TopicName = ?", name)
        rows = cursor.fetchall()

        if rows == None:
            return NOT_FOUND

        return [TopicSimple(
            row.TopicID or None,
            row.Name or None,
            row.Description or None
        ) for row in rows]

def delete(topic_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC DeleteTopic @TopicID = ?", topic_id)
            conn.commit()
        except IntegrityError:
            print("Error: ", e)
            raise        

def generate_topic_id(name: str, description: str) -> str:
    # Combine name and description
    combined = f"{name}{description}"
    # Generate SHA-256 hash of the combined string
    hash_object = hashlib.sha256(combined.encode())
    # Get the first 10 characters of the hex digest
    topic_id = hash_object.hexdigest()[:10]
    return topic_id

def update(topic_id: str, topic: TopicForm):
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            EXEC UpdateTopic @TopicID = ?, @Name = ?, @Description = ?;
            """,
            topic_id, topic.Name, topic.Description
        )

        conn.commit()

