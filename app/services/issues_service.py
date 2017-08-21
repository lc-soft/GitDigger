from app import app, db, csrf
from app.models.issue import Issue
from lib.utils import datetime_from_utc
from lib.markdown import markdown
from app.services import users_service
from app.services import topics_service
from app.services import repositories_service as repos_service

def get(issue_id):
    return Issue.query.get(issue_id)

def get_by_origin_id(origin_id):
    return Issue.query.filter_by(origin_id=origin_id).first()

def create(data, repo):
    user = users_service.get(data['user']['id'])
    if user is None:
        user = users_service.create(data['user'])
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return None
    issue = Issue(user, repo, data)
    try:
        issue.body_html = markdown(issue.body)
        db.session.add(issue)
        db.session.commit()
    except:
        db.session.rollback()
        return None
    for topic in issue.topics:
        topics_service.update_issues_count(topic)
    db.session.commit()
    return issue

def update(issue, data):
    issue.state = data['state']
    issue.title = data['title']
    issue.body = data['body']
    issue.body_html = markdown(issue.body)
    issue.comments_count = data['comments']
    issue.updated_at = datetime_from_utc(data['updated_at'])
