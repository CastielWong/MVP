#!/usr/bin/env bash
PYTHON_VERSION="3.8.6"
PYENV_VENV="dev-mvp"

if ! command -v pyenv &> /dev/null; then
  echo "pyenv not found. Start downloading..."

  # disable SSL verification if issue "SSL certificate problem" is encountered
#   git config --global http.sslVerify false
  default_git_ssl_value=${GIT_SSL_NO_VERIFY}
  export GIT_SSL_NO_VERIFY=true
  curl -k -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
  # reset the environment variable back
  export GIT_SSL_NO_VERIFY=${default_git_ssl_value}

  echo -e "\n\n# setup for pyenv" >> ~/.bashrc
  echo -e "export PATH=\"${HOME}/.pyenv/bin:${PATH}\"" >> ~/.bashrc
  echo -e 'eval "$(pyenv init -)"' >> ~/.bashrc
  echo -e 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

  source "${HOME}/.bashrc"

  # prerequisites - https://github.com/pyenv/pyenv/wiki/Common-build-problems
  yum install -y \
  @development zlib-devel bzip2 bzip2-devel readline-devel sqlite \
  sqlite-devel openssl-devel xz xz-devel libffi-devel findutils
fi
echo "pyenv has been installed"

# check if the specified venv exists
pyenv versions | grep ${PYENV_VENV}

is_venv_existed=$?
# set up the virtual environment if not
if [ ${is_venv_existed} != 0 ]; then
  pyenv install -v ${PYTHON_VERSION}
  pyenv virtualenv ${PYTHON_VERSION} ${PYENV_VENV}
fi
pyenv activate ${PYENV_VENV}
echo "venv \"${PYENV_VENV}\" is activated"
