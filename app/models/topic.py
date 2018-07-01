from app import db
from flask import Flask

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    group = db.Column(db.String(80))
    issues_count = db.Column(db.Integer, default=0)
    repositories_count = db.Column(db.Integer, default=0)
    followers_count = db.Column(db.Integer, default=0)
    snippets_count =  db.Column(db.Integer, default=0)
    description = db.Column(db.String(1024))

    def __init__(self, name, group='default'):
        self.name = name
        self.group = group

    def __repr__(self):
        return '<Topic %r>' % self.name
