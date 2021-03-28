
# Url entity extractor

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

Also available here: https://url-entity-extractor-m4kand2eyq-et.a.run.app/docs

## Endpoints

### POST `/extract`

requires a JSON body with key `"url"`.
If the url returns a body, entity extraction is ran on it.
Entities are returned as an array of strings.
Furthermore, past successful queries are persisted and can be retrieved via the endpoint below.


### GET `/all-extracted`

Get all successful previous queries.


## The repo

### Make targets

- `make build`: build the image

- `make run`: runs the service

- `make freeze`: pin dependencies from `requirements.dev.txt`

- `make test`: builds the images and runs unit and integration tests