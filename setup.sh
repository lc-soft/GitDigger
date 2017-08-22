#!/bin/sh
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install build-essential libffi-dev python-dev postgresql postgresql-server-dev-all redis-server nodejs
sudo pip install setuptools pipenv uwsgi
pipenv install

mkdir log
mkdir db/migrate/versions
