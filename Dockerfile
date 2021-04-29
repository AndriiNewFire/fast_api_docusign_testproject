FROM python:3.9-buster
MAINTAINER Andrii Divnych

ENV PYTHONUNBUFFERED 1

COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock

RUN pip install pipenv && pipenv install --system --deploy

WORKDIR /app
COPY ./app /app
