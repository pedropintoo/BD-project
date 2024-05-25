import sys
sys.path.append('.')
import hashlib
import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from .session import create_connection

class Graph1(NamedTuple):
    DataSets: dict[str, list[str, int]]

class Graph2(NamedTuple):
    DataSets: dict[str, (str, int)] 
    max: int

class Graph3(NamedTuple):
    DataSets: dict[str, (int, int)]
    max: int


def Graph1Top3TopicsPerYear():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("EXEC Top3TopicsPerYear")
        
        rows = cursor.fetchall()

        data_sets = {}

        for row in rows:
            
            if row.PublicationYear not in data_sets:
                data_sets[row.PublicationYear] = []
            
            data_sets[row.PublicationYear].append((row.TopicName, row.TopicCount))
        
        return Graph1(data_sets)
    

def Graph2MostProductiveAuthorsByTopic():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("EXEC MostProductiveAuthorsByTopic")
        
        rows = cursor.fetchall()

        topics = []
        data_sets = {}

        for row in rows:

            if row.TopicName not in data_sets:
                data_sets[row.TopicName] = []
            
            data_sets[row.TopicName] = (row.AuthorName, row.ArticlesCount)
        
        return Graph2(data_sets, max([x[1] for x in data_sets.values()]))


def Graph3RunningCitationsSumPerTopic():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("EXEC RunningCitationsSumPerTopic")
        
        rows = cursor.fetchall()

        data_sets = {}

        for row in rows:
            
            if row.TopicName not in data_sets:
                data_sets[row.TopicName] = [0, 0]
            
            data_sets[row.TopicName][0] = row.CitationsCount
            data_sets[row.TopicName][1] += row.RunningCitationsSum
        
        max_value = data_sets[row.TopicName][1]

        return Graph3(data_sets, max_value)