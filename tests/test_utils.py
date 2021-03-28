import pytest

from src.utils import get_url_body, extract_entities, InvalidUrlException


def test_get_url_body(sample_url: str):
    body = get_url_body(sample_url)
    assert isinstance(body, str)


def test_get_url_body_exception():
    with pytest.raises(InvalidUrlException):
        _ = get_url_body("not_a_url") 


def test_extract_entities():
    entities = extract_entities("The Evergreen ship is stuck in Suez Canal.")
    
    assert len(entities) > 0
    for ent in entities:
        assert isinstance(ent, str)