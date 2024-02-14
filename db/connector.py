import sqlite3
from pathlib import Path
from sqlite3 import Error

script_path = Path(__file__).parent
db_path = script_path / 'main.sqlite'


def create_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        print('Connection to DB successful')
    except Error as e:
        print(f'Error: {e}')

    return connection


if __name__ == '__main__':
    create_connection(db_path)
