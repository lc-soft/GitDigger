#!/bin/sh
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install build-essential python-dev postgresql postgresql-server-dev-all redis-server nodejs
sudo pip install setuptools pipenv uwsgi
pipenv install
pipenv install flask flask-script psycopg2 flask-sqlalchemy flask-migrate github-flask flask-login flask-wtf flask_restful github-webhook celery redis

mkdir log
mkdir db/migrate/versions
