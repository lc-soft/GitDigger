from app import app, csrf, db
from app.services import repositories_service as repos_service
from app.services import webhook, issues_service, voters_service
from flask import jsonify, Blueprint, request
from flask_login import current_user

views = Blueprint('issues', __name__)

def update(data):
    issue = issues_service.get_by_origin_id(data['issue']['id'])
    if issue is not None:
        issues_service.update(issue, data['issue'])
        return True
    repo = repos_service.get_by_origin_id(data['repository']['id'])
    if repo is None:
        return False
    try:
        issue = issues_service.create(data['issue'], repo)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True

@webhook.hook()
def issues(data):
    try:
        if update(data):
            return 'ok'
        else:
            return 'faild', 500
    except:
        return 'faild', 500

app.register_blueprint(views)
