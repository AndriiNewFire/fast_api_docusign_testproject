FROM python:3.9-buster
MAINTAINER Andrii Divnych

ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock
RUN pipenv install --system --deploy

WORKDIR /app
COPY ./app /app

RUN adduser -D Andrii
USER Andrii