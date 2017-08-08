from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(32), nullable=False, default='STOPPED')
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), default='')
    target_id = db.Column(db.Integer, default=0)
    target_type = db.Column(db.String(64), default='system')
    progress = db.Column(db.Integer, default=0)
    current = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, target, description=''):
        if target:
            self.target_id = target.id
            self.target_type = target.__tablename__
        else:
            self.target_id = 0
            self.target_type = 'system'
        self.description = description
        self.name = name

    def update(self):
        self.progress = (self.current / self.total) * 100

    def start(self, total):
        self.total = total
        self.current = 0
        self.state = 'STARTED'
    
    def finish(self):
        self.state = 'STOPPED'
        self.progress = 100
        self.current = self.total

    def __repr__(self):
        return '<Task %r>' % self.name
