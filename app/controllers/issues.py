from app import app, db, csrf
from app.services import webhook
from app.models.issue import Issue
from app.helpers.application_helper import flash
from app.helpers.topics_helper import TopicsHelper
from app.helpers.users_helper import UsersHelper
from app.helpers.repositories_helper import RepositoriesHelper
from lib.utils import datetime_from_utc
from flask import request, redirect, abort, jsonify
from flask import Blueprint, url_for, render_template
from flask_login import login_required, current_user

views = Blueprint('issues', __name__)
repos_helper = RepositoriesHelper(app)
users_helper = UsersHelper(app)
topics_helper = TopicsHelper()

def create(data):
    issue = data['issue']
    user = users_helper.get_user(issue['user']['id'])
    if user is None:
        user = users_helper.create_user(issue['user'])
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return None
    repo = repos_helper.get_repo_by_id(data['repository']['id'])
    if repo is None:
        return None
    issue = Issue(user, repo, issue)
    try:
        db.session.add(issue)
        db.session.commit()
    except:
        db.session.rollback()
        return None
    for topic in issue.topics:
        topics_helper.update_issues_count(topic)
    db.session.commit()
    return issue

def update(data):
    action = data['action']
    issue = Issue.query.filter_by(origin_id=data['issue']['id']).first()
    if issue is None:
        issue = create(data)
        if issue is None:
            return False
    try:
        db.session.add(issue)
        db.session.commit()
        if action == 'opened':
            return True
    except:
        db.session.rollback()
        return False
    data = data['issue']
    issue.state = data['state']
    issue.title = data['title']
    issue.body = data['body']
    issue.comments_count = data['comments']
    issue.updated_at = datetime_from_utc(data['updated_at'])
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True

@webhook.hook()
def issues(data):
    if update(data):
        return 'ok'
    return 'faild', 500

# only for test add issue
@csrf.exempt
@app.route('/api/issues', methods=['POST'])
def new():
    data = request.get_json()
    return jsonify({ 'success': update(data) })

app.register_blueprint(views)
