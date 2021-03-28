import os
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest
import sqlite3

from src.main import app
from src.database import create_connection
from src.database import create_table


@pytest.fixture
def sample_url() -> str:
    return "https://api.chucknorris.io/jokes/_nHrivZuTuOebVVya0e2LA"
    # for a random joke, return "https://api.chucknorris.io/jokes/random"


@pytest.fixture
def test_client(tmp_db_path) -> TestClient:
    return TestClient(app)


@pytest.fixture
def tmp_db_path(tmpdir: Path) -> Path:
    p = Path(tmpdir) / "test_database.db"

    yield p 

    if os.path.isfile(p):
        os.remove(p)
