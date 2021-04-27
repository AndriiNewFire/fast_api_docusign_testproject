FROM python:3.9-alpine
MAINTAINER Andrii Divnych

ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock
RUN pipenv install --system --deploy

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D Andrii
USER Andrii