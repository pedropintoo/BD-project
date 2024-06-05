import sys
sys.path.append('.')
 
import pyodbc
from persistency.session import create_connection
from tables import *

def drop_tables():
    for table in tables:
        with create_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"DROP TABLE {table}")
            except Exception as e:
                print("Table drop error.", e)
            cursor.commit()


if __name__ == '__main__':
    drop_tables()