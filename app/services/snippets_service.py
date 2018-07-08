from app import db
from app.models.snippet import Snippet
from app.models.voter import Voter
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func
from datetime import datetime

def get_rating_sum(s):
    try:
        return db.session.query(func.sum(Voter.value).label('rating'))\
            .filter(Voter.target_id==s.id)\
            .filter(Voter.target_type==s.__tablename__)\
            .group_by(Voter.target_id).one()[0]
    except NoResultFound:
        return 0

def update(s, data):
    s.file = data['file']
    s.line = data['line']
    s.language = data['language']
    s.content = data['content']
    s.content_start_line = data['content_start_line']
    s.content_end_line = data['content_end_line']
    s.description = data['description']
    s.commit_id = data['commit_id']
    s.updated_at = datetime.utcnow()
    return s

def find(repo_id):
    return Snippet.query.filter(Snippet.repository_id==repo_id)
