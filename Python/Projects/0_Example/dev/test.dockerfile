# Docker image used to run tests
FROM python:3.10.13

ARG PIP_REPO=https://pypi.org/simple/

# ARG REQUESTS_CA_BUDLE=/etc/ssl/certs/ca-bundle.crt
# ENV REQUESTS_CA_BUDLE=${REQUESTS_CA_BUDLE}

RUN apt-get update
# install pyodbc dependencies
RUN apt-get install -y unixodbc
RUN apt-get install -y vim


WORKDIR /app

COPY dev/requirements.txt /app/dev/requirements.txt
COPY requirements.txt /app/requirements.txt
COPY core /app/core

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt --index-url ${PIP_REPO} \
    && python -m pip install -r dev/requirements.txt --index-url ${PIP_REPO}
