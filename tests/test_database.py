from pathlib import Path
import json

import sqlite3

from src.database import create_connection, create_table, insert_new_log, list_tables, list_all_lines


def test_create_table(tmp_db_path: Path):
    table_name = "my_table"
    create_table(tmp_db_path, table_name=table_name)

    table_names = list_tables(tmp_db_path)
    assert table_name in table_names


def test_insert_new_log(tmp_db_path: Path):
    table_name = "my_table"
    create_table(tmp_db_path, table_name=table_name)

    logs = [
        ("http://url1.com", ["ent1", "ent2"]),
        ("http://url2.com", ["ent4", "ent2"]),
        ("http://url3.com", ["ent3", "ent4"]),
        ("http://url4.com", ["ent1"]),
        ("http://url5.com", []),
    ] 

    for log in logs:
        insert_new_log(
            url=log[0],
            entities=log[1],
            db_path=tmp_db_path,
            table_name=table_name
            )
    
    db_logs = list_all_lines(tmp_db_path, table_name=table_name)

    assert len(logs) == len(db_logs)
    
    for log, db_log in zip(logs, db_logs):
        assert log[0] == db_log[-2]
        assert log[1] == json.loads(db_log[-1])