import sys
sys.path.append('.')
 
import pyodbc
from persistency.session import create_connection

def readScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    return sqlFile.split(';')

def create_tables():
    scripts = readScriptsFromFile("tables/create_tables.sql")

    for command in scripts:
        with create_connection() as conn:
            cursor = conn.cursor()
            try:
                if command:
                    cursor.execute(command)
            except Exception as e:
                print("Table creation error.", e)
            cursor.commit()


if __name__ == '__main__':
    create_tables()