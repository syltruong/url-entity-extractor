SHELL := /bin/bash

IMAGE_NAME = entity-extractor


.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .


.PHONY: run
run: build
	docker run -p 8000:8000 $(IMAGE_NAME)


.PHONY: test
test: build
	docker run $(IMAGE_NAME) bash -c "cd app/ && pytest"


.PHONY: freeze
freeze:
	cp requirements.dev.txt requirements.txt
	docker build -t $(IMAGE_NAME) .
	docker run --rm $(IMAGE_NAME) cat requirements.txt > requirements.txt
