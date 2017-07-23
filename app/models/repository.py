from app import db
from app.models.user import User
from app.models.topic import Topic
from lib.utils import datetime_from_utc
from datetime import datetime
from flask import Flask

topics = db.Table('RepoTopics',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('repo_id', db.Integer, db.ForeignKey('repository.id'))
)

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))
    html_url = db.Column(db.String(1024))
    homepage = db.Column(db.String(256))
    pushed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    imported_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    owner = db.relationship(User, uselist=False)
    topics = db.relationship('Topic', secondary=topics,
        backref=db.backref('repos', lazy='dynamic'))

    def __init__(self, owner_id, data):
        self.name = data['name']
        self.homepage = data['homepage']
        self.html_url = data['html_url']
        self.owner_id = owner_id
        self.description = data['description']
        self.created_at = datetime_from_utc(data['created_at'])
        self.updated_at = datetime_from_utc(data['updated_at'])
        self.pushed_at = datetime_from_utc(data['pushed_at'])
        for name in data['topics']:
            topic = Topic.query.filter_by(name=name).first()
            if topic is None:
                topic = Topic(name)
            self.topics.append(topic)

    def __repr__(self):
        return '<Repository %r>' % self.full_name

