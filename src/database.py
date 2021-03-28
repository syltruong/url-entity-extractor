from datetime import datetime
import json
from pathlib import Path
from typing import Optional

import sqlite3

DB_PATH = Path(__file__).parent.parent.absolute() / "data" / "extracted_entities.db"
TABLE_NAME = "past_queries"


def create_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    print(db_path)
    conn = sqlite3.connect(db_path)

    return conn


def create_table(db_path: Path = DB_PATH, table_name: str = TABLE_NAME):
    
    # Note that by setting the id as primary key, the key autoincrements by default
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id integer PRIMARY KEY,
        date text,
        url text,
        entities text
    )
    """

    conn = create_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)


def list_tables(db_path: Path = DB_PATH) -> list[str]:

    sql = "SELECT name FROM sqlite_master WHERE type='table';"

    conn = create_connection(db_path)
    cursor = conn.cursor()
    result = cursor.execute(sql).fetchall()
    table_names = [elt[0] for elt in result]

    return table_names


def insert_new_log(
    url: str, 
    entities: list[str], 
    db_path: Path = DB_PATH, 
    table_name: str = TABLE_NAME
    ):

    create_table(db_path=db_path, table_name=table_name)

    sql = f"""
        INSERT INTO {table_name}(id, date, url, entities)
        VALUES(NULL, ?, ?, ?)
    """

    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    entities = json.dumps(entities)

    conn = create_connection(db_path)
    cursor = conn.cursor()
    new_log = (date, url, entities)
    cursor.execute(sql, new_log)
    conn.commit()


def list_all_lines(db_path: Path = DB_PATH, table_name: str = TABLE_NAME) -> list[tuple]:

    conn = create_connection(db_path) 
    cursor = conn.cursor()
    all_lines = cursor.execute(f"SELECT * FROM {table_name}").fetchall()

    return all_lines