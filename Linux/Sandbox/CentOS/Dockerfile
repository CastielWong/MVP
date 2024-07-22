FROM centos:8

# customization
ENV VERSION_MAJOR_MINOR=3.8
ARG VERSION_FULL=${VERSION_MAJOR_MINOR}.6

# install common tools
RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

RUN yum update -y
RUN yum install -y \
    make wget \
    vim

# -------------------------------------------------------------------------------------
# setup to use systemd
ENV container docker

RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

VOLUME [ "/sys/fs/cgroup" ]

CMD ["/usr/sbin/init"]

# -------------------------------------------------------------------------------------
# install Python
WORKDIR /root

# "sqlite-devel" is used to fix "No module named '_sqlite3'" issue
RUN yum install -y \
    tar gcc openssl-devel bzip2-devel libffi-devel \
    sqlite-devel


# download and extract Python source
RUN wget https://www.python.org/ftp/python/${VERSION_FULL}/Python-${VERSION_FULL}.tgz && \
    tar -xzf Python-${VERSION_FULL}.tgz

# configure, build, and install Python
WORKDIR /root/Python-${VERSION_FULL}
RUN ./configure --enable-optimizations && \
    make altinstall

# clean up
WORKDIR /root
RUN rm -rf Python-${VERSION_FULL} Python-${VERSION_FULL}.tgz

# # ensure Python is in PATH
# RUN ln -s /usr/local/bin/python${VERSION_MAJOR_MINOR} /usr/local/bin/python && \
#     ln -s /usr/local/bin/pip${VERSION_MAJOR_MINOR} /usr/local/bin/pip

# update pip and make alias for Python
RUN echo $'\n# customization' >> /root/.bashrc
RUN echo 'alias python3=python${VERSION_MAJOR_MINOR}' >> /root/.bashrc
RUN echo 'alias pip="python3 -m pip"' >> /root/.bashrc

# -------------------------------------------------------------------------------------

RUN python${VERSION_MAJOR_MINOR} -m pip install --upgrade \
    pip setuptools wheel

# curtomize the bash prompt
RUN echo 'export PS1="[\t \u@\h \w]\$ "'  >> /root/.bashrc

WORKDIR /root
