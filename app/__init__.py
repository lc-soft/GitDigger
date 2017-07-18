import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

def Database():
    path = os.path.abspath(os.path.join(__file__, '..', '..'))
    path = os.path.join(path, 'db', 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    return db

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

db = Database()
migrate = Migrate(app, db, directory='db/migrate')

from app import models
from app import controllers
