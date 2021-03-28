from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.database import create_table

def test_invalid_url(test_client: TestClient):
    response = test_client.post(
        "/extract",
        json={"url" : "some_invalid_url"}
    )
    assert response.status_code == 400  # bad request


def test_invalid_json_keys(test_client: TestClient, sample_url: str):
    response = test_client.post(
        "/extract",
        json={"not_url" : sample_url}
    )
    assert response.status_code == 422  # unprocessable entry


def test_extract(test_client: TestClient, sample_url: str, tmp_db_path: Path):

    #
    # need to set the app to use the tmp_db_path
    #

    with patch("src.main.DB_PATH", tmp_db_path):
        response = test_client.post(
            "/extract",
            json={"url" : sample_url}
            )
    
    assert response.status_code == 200

    response_json = response.json()

    assert "body" in response_json
    assert "entities" in response_json
    
    assert isinstance(response_json["body"], str)
    
    if len(response_json["entities"]) > 0:
        for ent in response_json["entities"]:
            assert isinstance(ent, str)
    
    assert "Chuck Norris" in response_json["entities"]

    with patch("src.main.DB_PATH", tmp_db_path):
        all_extracted = test_client.get("/all-extracted").json()

    print(all_extracted)
    assert len(all_extracted) == 1


def test_all_extracted(test_client: TestClient, sample_url: str, tmp_db_path: Path):
    
    n = 5

    with patch("src.main.DB_PATH", tmp_db_path):
        for _ in range(n):
            test_client.post(
                "/extract",
                json={"url" : sample_url}
                )
        
        response = test_client.get("/all-extracted")
    
    assert response.status_code == 200 

    response_json = response.json()
    print(response_json)
    assert len(response_json) == 5
    assert len(set([elt["id"] for elt in response_json])) == n
    assert len(set([elt["url"] for elt in response_json])) == 1
