FROM python:3.10.13

ARG PIP_REPO=https://pypi.org/simple/

RUN apt-get update
RUN apt install -y \
    vim \
    unixodbc

WORKDIR /app

COPY dev/requirements.txt /app/requirements.txt
COPY src /app/src

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --index-url ${PIP_REPO}
