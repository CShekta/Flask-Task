#! /usr/bin/env bash

set -e

sudo apt-get update
sudo apt-get install -y tar curl git

# Libraries required to build a complete python with pyenv:
# https://github.com/yyuu/pyenv/wiki
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev

# Install pyenv
if [ ! -d ~/.pyenv ]; then
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv
fi
echo '
# Pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
' >> ~/.bash_profile
source ~/.bash_profile
hash

pushd /vagrant

    # Install our python version
    pyenv install -s # skip existing version
    pyenv rehash

    # Install a virtualenv
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate

    # Lastly, our dependencies
    pip install -r requirements.txt

popd
