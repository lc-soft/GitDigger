#!/bin/sh
echo "install dependencies ..."
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y build-essential libffi-dev python-dev postgresql postgresql-server-dev-all nginx redis-server python-pip nodejs
sudo pip install setuptools pipenv uwsgi
pipenv install

mkdir log
mkdir tmp
mkdir db/migrate/versions

echo "create default config file ..."
cp config/github.py.example config/github.py
cp config/database.py.postgresql.example config/database.py

echo "create database ..."
sudo -u postgres createuser gitdigger -P
sudo -u postgres createdb -O gitdigger gitdigger_development
