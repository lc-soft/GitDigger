from app import app, csrf
from app.services import webhook
from app.services import issues_service
from app.services import repositories_service
from flask import jsonify, Blueprint, request

views = Blueprint('issues', __name__)

def update(data):
    issue = issues_service.get(data['issue']['id'])
    if issue is not None:
        issues_service.update(issue, data['issue'])
        return True
    repo = repositories_service.get_by_id(data['repository']['id'])
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
