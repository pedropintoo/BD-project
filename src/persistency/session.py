import configparser
import functools
from pathlib import Path
import os

import pyodbc


@functools.cache
def conn_string() -> str:
    config_file = Path("conf.ini")
    assert config_file.exists(), "conf.ini file not found"

    config = configparser.ConfigParser(os.environ)
    config.read(config_file)

    server = config["database"]["server"]
    db_name = config["database"]["name"]
    username = config["database"]["username"]
    password = config["database"]["password"]

    return f"DRIVER={{SQL Server}};SERVER={server};DATABASE={db_name};UID={username};PWD={password};charset='utf8'"


def create_connection():
    my_conn_string = conn_string()
    return pyodbc.connect(my_conn_string)

# if __name__ == "__main__":
#     print(conn_string())