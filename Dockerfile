FROM python:3.9.0

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . app/
CMD cd app/ && uvicorn src.main:app --reload --host 0.0.0.0