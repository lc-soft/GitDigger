from app import db
from lib.utils import datetime_from_utc
from datetime import datetime

topics = db.Table('IssueTopics',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('issue_id', db.Integer, db.ForeignKey('issue.id'))
)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(32), nullable=False, default='open')
    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.String(4096), default='')
    body_html = db.Column(db.String(4096), default='')
    repository = db.relationship('Repository', uselist=False)
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'),
                              nullable=False)
    user = db.relationship('User', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    html_url = db.Column(db.String(256), nullable=False)
    comments_count = db.Column(db.Integer, default=0)
    topics = db.relationship('Topic', secondary=topics,
                             backref=db.backref('issue', lazy='dynamic'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user, repo, data):
        self.user = user
        self.user_id = user.id
        self.repository = repo
        self.repository_id = repo.id
        self.topics = repo.topics
        self.origin_id = data['id']
        self.number = data['number']
        self.state = data['state']
        self.body = data['body']
        self.title = data['title']
        self.html_url = data['html_url']
        self.comments_count = data['comments']
        self.created_at = datetime_from_utc(data['created_at'])
        self.updated_at = datetime_from_utc(data['updated_at'])

    def __repr__(self):
        return '<Issue %r (%r)>' % (self.title, self.number)
