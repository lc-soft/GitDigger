#!/bin/sh
pip install flask flask-script psycopg2 flask-sqlalchemy flask-migrate github-flask flask-login flask-wtf flask_restful gitHub-webhook celery redis
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
apt-get install python-dev postgresql postgresql-server-dev-all redis-server nodejs
