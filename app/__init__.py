import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder="../static")
config.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory='db/migrate')

from app import models
from app import controllers
