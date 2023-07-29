# Docker image set for Airflow Kubernetes operator
FROM python:3.8.14

ARG PIP_REPO=https://pypi.org/simple/

WORKDIR /app

COPY dev/requirements.txt /app/dev/requirements.txt
COPY requirements.txt /app/requirements.txt
COPY core /app/core

RUN pip install --upgrade pip \
    && pip install -r dev/requirements.txt --index-url ${PIP_REPO} \
    && pip install -r requirements.txt --index-url ${PIP_REPO}
