from app import db
from datetime import datetime

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, default=1)
    target_id = db.Column(db.Integer)
    target_type = db.Column(db.String(64))
    user = db.relationship('User', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user, target):
        self.user = user
        self.user_id = user.id
        self.target_id = target.id
        self.target_type = target.__tablename__

    def __repr__(self):
        return '<Voter user_id="%r" target_type="%s" value="%d">' % (
            self.user_id, self.target_type, self.value
        )
