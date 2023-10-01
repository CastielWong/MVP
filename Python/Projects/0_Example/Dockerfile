# Docker image set for Airflow Kubernetes operator
FROM python:3.8.14

# ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-bundle.crt

ARG PIP_REPO=https://pypi.org/simple/
ARG USER_NAME=castiel

RUN apt-get update
RUN apt-get install -y vim

# create a user to avoid root privilege
RUN useradd --create-home ${USER_NAME}
USER ${USER_NAME}

ENV VIRTUALENV=/home/${USER_NAME}/venv
RUN python3 -m venv ${VIRTUALENV}
ENV PATH="${VIRTUALENV}/bin:${PATH}"

# # set link if there is not
# RUN ln -s /usr/bin/python3 /usr/bin/python \
#     & ln -s /usr/bin/pip3 /usr/bin/pip


WORKDIR /app

COPY --chown=${USER_NAME} requirements.txt /app/requirements.txt
COPY --chown=${USER_NAME} dev/requirements.txt /app/dev/requirements.txt
COPY --chown=${USER_NAME} core /app/core

RUN python -m pip install --upgrade pip setuptools \
    && python -m pip install -r requirements.txt --index-url ${PIP_REPO} \
    && python -m pip install -r dev/requirements.txt --index-url ${PIP_REPO}
