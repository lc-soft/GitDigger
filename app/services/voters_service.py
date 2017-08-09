from app.models.voter import Voter

def get(user, target):
    return Voter.query.filter_by(
        user_id=user.id, target_id=target.id, 
        target_type=target.__tablename__
    ).first()
