from config import points
from app.models.voter import Voter
from app.models.point_log import PointLog
from app.services import webhook, users_service
from app.services import issues_service, voters_service
from app.services import repositories_service as repos_service
from app import app, csrf, db, login_manager
from flask import jsonify, Blueprint, request
from flask_login import current_user

views = Blueprint('issues', __name__)

@views.route('/api/issues/<string:issue_id>/voters/<string:username>', 
             methods=['PUT', 'DELETE'])
def vote(issue_id, username):
    if not current_user.is_authenticated:
        return jsonify({'status': 401, 'msg': 'permission denied'})
    issue = issues_service.get(issue_id)
    if issue is None:
        return jsonify({'status': 400, 'msg': 'issue not found'})
    user = users_service.get_by_username(username)
    if user is None:
        return jsonify({'status': 400, 'msg': 'user not found'})
    action = request.args.get('action', 'upvote')
    value = -1 if action == 'downvote' else 1
    voter = voters_service.get(user, issue)
    if voter is None:
        if current_user.points < points.VOTE:
            return jsonify({'status': 403, 'msg': 'points are not enough'})
        log = PointLog(action, points.VOTE, user, issue)
        voter = Voter(user, issue)
        db.session.add(voter)
        db.session.add(log)
        issue.points += value
    elif voter.value != value:
        issue.points += value
    voter.value = value
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'status': 500, 'msg': 'operation failed'})
    return jsonify({'status': 0, 'msg': 'success'})

def update(data):
    issue = issues_service.get_by_origin_id(data['issue']['id'])
    if issue is not None:
        issues_service.update(issue, data['issue'])
        return True
    repo = repos_service.get_by_origin_id(data['repository']['id'])
    if repo is None:
        return False
    issue = issues_service.create(data['issue'], repo)
    if issue is None:
        return False
    try:
        db.session.add(issue)
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

# only for test add issue
@csrf.exempt
@app.route('/api/issues', methods=['POST'])
def new():
    data = request.get_json()
    return jsonify({ 'success': update(data) })

app.register_blueprint(views)
