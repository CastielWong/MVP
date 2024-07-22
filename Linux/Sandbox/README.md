
"Dockerfile" is used to create an CentOS image with Python installed.

If it's a different Linux flavor using `apt`, below is the steps to install Python:
```sh
# https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/
apt update
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

VERSION=3.10.14
wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz

tar -xf Python-$VERSION.tgz

cd  Python-$VERSION/
./configure --enable-optimizations

make -j $(nproc)
make altinstall
```
