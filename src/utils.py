import requests

import spacy

NLP = spacy.load("en_core_web_sm")


def get_url_body(url: str) -> str:
    """
    Get body from url

    Parameters
    ----------
    url : str
        source url

    Returns
    -------
    str
        body

    Raises
    ------
    InvalidUrlException
        Raised when body could not be retrieved
    """

    try: 
        response = requests.get(url)
    except Exception as e:
        raise InvalidUrlException("Could not get a response from the url provided", e)

    return response.text


def extract_entities(body: str) -> list[str]:
    """
    Extract named entities from body

    Parameters
    ----------
    body : str
        body

    Returns
    -------
    list[str]
        list of entities
    """

    body = NLP(body)

    entities = [ent.text for ent in body.ents]
    
    return entities


class InvalidUrlException(Exception):
    """ Raised when the target url could not be reached """
    