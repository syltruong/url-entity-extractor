import json
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

from src.utils import get_url_body, InvalidUrlException, extract_entities
from src.database import create_connection, create_table, insert_new_log, list_all_lines, DB_PATH


class Source(BaseModel):
    url: str

app = FastAPI()


@app.post("/extract")
def extract(source: Source):

    try:
        body = get_url_body(source.url)
        entities = extract_entities(body)
        ret = {
            "body" : body,
            "entities" : entities
        }
    except InvalidUrlException as e:
        raise HTTPException(status_code=400, detail=f"Bad Request, {e}")

    insert_new_log(db_path=DB_PATH, url=source.url, entities=entities)

    return ret


@app.get("/all-extracted")
def all_extracted():

    try:
        all_lines = list_all_lines(db_path=DB_PATH)
    except sqlite3.OperationalError:
        all_lines = []

    ret = [
        {
            "id" : elt[0],
            "date" : elt[1],
            "url" : elt[2],
            "entities" : json.loads(elt[3]), 
        }
        for elt in all_lines
    ]

    return ret
