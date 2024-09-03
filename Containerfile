FROM python:3-alpine3.20 AS base

WORKDIR /app

FROM base AS reqs 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM reqs AS app
COPY templates templates
COPY wsgi.py wsgi.py

VOLUME images

ENTRYPOINT waitress-serve wsgi:app

