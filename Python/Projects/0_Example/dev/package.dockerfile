# Docker image used to build and publish package
FROM python:3.10.13

ARG PIP_REPO=https://pypi.org/simple/


WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY core /app/core

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --index-url ${PIP_REPO}
