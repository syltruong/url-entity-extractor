FROM python:3.9.0

copy requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip freeze > requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . app/
ENV PORT=8080
CMD cd app/ && uvicorn src.main:app --reload --host 0.0.0.0 --port 8080