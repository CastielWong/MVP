# Docker image used to run tests
FROM python:3.8.14

ARG PIP_REPO=https://pypi.org/simple/


# pyodbc dependencies
RUN apt-get update
RUN apt-get install -y unixodbc
RUN apt-get install -y vim


WORKDIR /app

COPY dev/requirements.txt /app/dev/requirements.txt
COPY dev/.coveragerc /app/dev/.coveragerc
COPY requirements.txt /app/requirements.txt
COPY core /app/core

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt --index-url ${PIP_REPO} \
    && python -m pip install -r dev/requirements.txt --index-url ${PIP_REPO}
