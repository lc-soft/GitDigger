import config
from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder='../static')
config.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory='db/migrate')

worker = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
worker.conf.update(app.config)

from app import models
from app import helpers
from app import filters
from app import services
from app import controllers
from app import workers
from app import api

filters.init_app(app)
