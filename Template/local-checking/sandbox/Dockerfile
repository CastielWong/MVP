
FROM debian:11.10-slim

# customization
ENV VERSION_MAJOR_MINOR=3.11
ARG VERSION_FULL=${VERSION_MAJOR_MINOR}.9
ARG PIP_REPO=https://pypi.org/simple/
ARG USER_NAME=castiel

# install common tools
RUN apt-get update
RUN apt install -y \
    wget \
    vim

# -------------------------------------------------------------------------------------
# install Python
WORKDIR /root

RUN apt install -y \
    build-essential zlib1g-dev \
    libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
    libreadline-dev libffi-dev libsqlite3-dev libbz2-dev

# download and extract Python source
RUN wget https://www.python.org/ftp/python/${VERSION_FULL}/Python-${VERSION_FULL}.tgz && \
    tar -xf Python-${VERSION_FULL}.tgz

# configure, build, and install Python
WORKDIR /root/Python-${VERSION_FULL}
RUN ./configure --enable-optimizations && \
    make -j $(nproc) && \
    make altinstall

# clean up
WORKDIR /root
RUN rm -rf Python-${VERSION_FULL} Python-${VERSION_FULL}.tgz

# ensure Python is in PATH
RUN ln -s /usr/local/bin/python${VERSION_MAJOR_MINOR} /usr/local/bin/python && \
    ln -s /usr/local/bin/pip${VERSION_MAJOR_MINOR} /usr/local/bin/pip

# -------------------------------------------------------------------------------------

RUN python${VERSION_MAJOR_MINOR} -m pip install --upgrade \
    pip setuptools wheel

# curtomize the bash prompt
RUN echo 'export PS1="[\\t \u@\h \w]\$ "'  >> /root/.bashrc

WORKDIR /root
