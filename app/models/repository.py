from app import db
from app.models.topic import Topic
from lib.utils import datetime_from_utc
from datetime import datetime

topics = db.Table('repository_topics',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('repo_id', db.Integer, db.ForeignKey('repository.id'))
)

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))
    logo_url = db.Column(db.String(256))
    html_url = db.Column(db.String(256))
    homepage = db.Column(db.String(256))
    language = db.Column(db.String(32))
    last_snippet_number = db.Column(db.Integer, nullable=False, default=0)
    pushed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    imported_at = db.Column(db.DateTime, default=datetime.utcnow)
    imported_from = db.Column(db.String(16))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', uselist=False)
    topics = db.relationship('Topic', secondary=topics,
        backref=db.backref('repository', lazy='dynamic'))

    def __init__(self, owner, data):
        self.name = data['name']
        self.origin_id = data['id']
        self.homepage = data['homepage']
        self.language = data['language']
        self.html_url = data['html_url']
        self.description = data['description']
        self.created_at = datetime_from_utc(data['created_at'])
        self.updated_at = datetime_from_utc(data['updated_at'])
        self.pushed_at = datetime_from_utc(data['pushed_at'])
        self.owner_id = owner.id
        self.owner = owner
        language = data['language']
        has_language_topic = False
        for name in data['topics']: 
            topic = Topic.query.filter_by(name=name).first()
            if topic is None:
                topic = Topic(name)
                if language and name == language:
                    topic.group = 'language'
                    has_language_topic = True
                topic.repositories_count = 1
            self.topics.append(topic)
        if language and not has_language_topic:
            topic = Topic.query.filter_by(name=language).first()
            if topic is None:
                topic = Topic(language, 'language')
                topic.repositories_count = 1
            self.topics.append(topic)

    def __repr__(self):
        return '<Repository %r>' % self.name
