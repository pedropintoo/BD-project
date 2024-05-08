import sys
sys.path.append('.')
 
import pyodbc
from persistency.session import create_connection
from tables import *

def clear_tables():
    for table in tables:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table}")
            cursor.commit()


if __name__ == '__main__':
    clear_tables()