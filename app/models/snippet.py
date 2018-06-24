from app import db
from datetime import datetime

topics = db.Table('snippet_topics',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('snippet_id', db.Integer, db.ForeignKey('snippet.id'))
)

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(512), default='')
    content = db.Column(db.String(4096), default='')
    language = db.Column(db.String(32), nullable=False, default='text')
    repository = db.relationship('Repository', uselist=False)
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'),
                              nullable=False)
    file = db.Column(db.String(256), nullable=False)
    line = db.Column(db.Integer, nullable=False)
    content_start_line = db.Column(db.Integer, nullable=False)
    content_end_line = db.Column(db.Integer, nullable=False)
    commit_id = db.Column(db.String(40), nullable=False)
    rating = db.Column(db.Integer, default=60)
    ratings_count = db.Column(db.Integer, default=0)
    topics = db.relationship('Topic', secondary=topics,
                             backref=db.backref('snippet', lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, repo, data):
        repo.last_snippet_number += 1
        self.number = repo.last_snippet_number
        self.repository = repo
        self.repository_id = repo.id
        self.topics = repo.topics
        self.file = data['file']
        self.line = data['line']
        self.content_start_line = data['content_start_line']
        self.content_end_line = data['content_end_line']
        self.content = data['content']
        self.description = data['description']
        self.commit_id = data['commit_id']

    def __repr__(self):
        return '<Snippet %r (%r)>' % (self.title, self.id)
