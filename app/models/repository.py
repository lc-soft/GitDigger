from app import db
from app.models.user import User
from app.models.topic import Topic
from flask import Flask

topics = db.Table('RepoTopics',
	db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
	db.Column('repo_id', db.Integer, db.ForeignKey('repository.id'))
)

class Repository(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	description = db.Column(db.String(1024))
	html_url = db.Column(db.String(1024))
	homepage = db.Column(db.String(256))
	pushed_at = db.Column(db.DateTime)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	onwer_id = db.Column(db.Integer, db.ForeignKey(User.id))
	owner = db.relationship(User, uselist=False)
	tags = db.relationship('Topic', secondary=topics,
		backref=db.backref('repos', lazy='dynamic'))
	
	def __init__(self, onwer_id, name, description, homepage,
				 html_url, created_at, updated_at, pushed_at, tags=[]):
		self.name = name
		self.homepage = homepage
		self.html_url = html_url
		self.owner_id = owner_id
		self.description = description
		self.created_at = created_at
		self.updated_at = updated_at
		self.pushed_at = pushed_at
		for tagname in tags:
			tag = Tag.query.filter_by(name=tagname).first()
			if tag is None:
				tag = Tag(tagname)
			self.tags.append(tag)

	def __repr__(self):
		return '<Repository %r>' % self.full_name

