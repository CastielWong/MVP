

- [Installation](#installation)
- [Reference](#reference)

This section is to save all MVPs and cached knowledge related to Python.


# Installation

Install Python in Linux is a bit trivial, commands below is more than enough to install Python successfully.
 
```sh
yum install gcc openssl-devel bzip2-devel libffi-devel –y
 
wget https://www.python.org/ftp/python/3.x.x/Python-3.x.x.tgz
tar -xzf Python-3.x.x.tgz

./configure --enable-optimizations
make altinstall
```


## Reference

- How to Install Python 3: https://www.liquidweb.com/kb/how-to-install-python-3-on-centos-7/
