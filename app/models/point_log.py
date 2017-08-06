from app import db
from datetime import datetime

class PointLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(32))
    points = db.Column(db.Integer)
    sender_id = db.Column(db.Integer)
    sender_type = db.Column(db.String(32))
    receiver_id = db.Column(db.Integer)
    receiver_type = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, reason, points, sender, receiver):
        self.reason = reason
        self.points = points
        if sender:
            self.sender_id = sender.id
            self.sender_id = sender.id
            self.sender_type = sender.__tablename__
        else:
            self.sender_id = 0
            self.sender_type = 'system'
        if receiver:
            self.receiver_id = receiver.id
            self.receiver_type = receiver.__tablename__
        else:
            self.receiver_id = 0
            self.receiver_type = 'system'

    def __repr__(self):
        return '<PointLog %r>' % self.id
