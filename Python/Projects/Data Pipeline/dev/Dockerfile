FROM python:3.10.13

ARG PIP_REPO=https://pypi.org/simple/
# ARG USER_NAME=castiel

# install software needed for development
RUN apt-get update
RUN apt install -y vim

# install libodbc.so, libtdsS.so, isql, and isqlinst
RUN apt install -y unixodbc
    # unixodbc-dev freetds-dev freetds-bin

# install libtsdsodbc.so and tsq
RUN apt install -y tdsodbc

# # create a user to avoid root privilege
# RUN useradd --create-home ${USER_NAME}
# USER ${USER_NAME}

ENV VIRTUALENV=/home/${USER_NAME}/venv
RUN python3 -m venv ${VIRTUALENV}
ENV PATH="${VIRTUALENV}/bin:${PATH}"

# config driver for databases
COPY etc/odbcinst.ini /etc/odbcinst.ini

# bake the image with project
WORKDIR /app

COPY dev/requirements.txt /app/requirements.txt
COPY src /app/src

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --index-url ${PIP_REPO}
