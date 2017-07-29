from app import db
from flask import Flask
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80))
    bio = db.Column(db.String(180))
    github_id = db.Column(db.Integer, unique=True)
    github_username = db.Column(db.String(64), unique=True)
    github_token = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(300))
    created_at = db.Column(db.DateTime)

    def __init__(self, username, email, password, name=None):
        self.email = email
        self.username = username
        self.password = password
        if name is None:
            self.name = username
        else:
            self.name = name
        self.created_at = datetime.now()

    is_authenticated = True
    is_anonymous =  False
    is_active = True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username
