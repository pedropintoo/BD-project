import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection

class Graph1(NamedTuple):
    Topics: list[str]
    DataSets: dict[str, list[str, int]]

def Graph1Top3TopicsPerYear():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("EXEC Top3TopicsPerYear")
        
        rows = cursor.fetchall()

        topics = []
        data_sets = {}

        for row in rows:
            if row.TopicName not in topics:
                topics.append(row.TopicName)
            
            if row.PublicationYear not in data_sets:
                data_sets[row.PublicationYear] = []
            
            data_sets[row.PublicationYear].append((row.TopicName, row.TopicCount))
        
        return Graph1(topics, data_sets)

