import requests

from app import db
from app.models.voter import Voter
from app.models.point_log import PointLog
from app.api import api, resource_fields
from app.services import users_service, issues_service, \
    voters_service, repositories_service as repos_service

from flask_restful import Resource, marshal_with, abort, reqparse
from flask_login import current_user
from config import points

class Issues(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('html_url')

    @marshal_with(resource_fields.issue_fields)
    def post(self):
        args = self.parser.parse_args()
        url = args.get('html_url')
        url = url.replace('//github.com/', '//api.github.com/repos/')
        if current_user.points - points.IMPORT_ISSUE < 0:
            return abort(403, message='points are not enough')
        if url.find('//api.github.com/repos/') < 0:
            return abort(400, message='invalid issue url')
        if not current_user.is_authenticated:
            return abort(401, message='permission denied')
        try:
            result = requests.get(url, timeout=10)
            data = result.json()
        except:
            return abort(400, message='failed to get issue')
        issue = issues_service.get_by_origin_id(data['id'])
        if issue is not None:
            return abort(400, message='issue already exists')
        try:
            result = requests.get(data['repository_url'], timeout=10)
            repo = result.json()
        except:
            return abort(400, message='failed to get repository')
        repo = repos_service.get_by_origin_id(repo['id'])
        if repo is None:
            return abort(400, message='repository does not exist')
        log = PointLog('import_issue', points.IMPORT_ISSUE, current_user)
        current_user.points -= points.IMPORT_ISSUE
        try:
            issues_service.create(data, repo)
            db.session.add(log)
            db.session.commit()
        except:
            db.session.rollback()
            return abort(500, message='issue creation failed')
        return issue

class IssueVoters(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('action')

    @marshal_with(resource_fields.voter_fields)
    def put(self, issue_id, username):
        pt = points.VOTE
        if not current_user.is_authenticated:
            return abort(401, message='permission denied')
        issue = issues_service.get(issue_id)
        if issue is None:
            return abort(400, message='issue not found')
        user = users_service.get_by_username(username)
        if user is None:
            return abort(400, message='user not found')
        args = self.parser.parse_args()
        action = args.get('action')
        action = 'upvote' if action is None else action
        value = -1 if action == 'downvote' else 1
        voter = voters_service.get(user, issue)
        if voter is None:
            if current_user.points - pt < 0:
                return abort(403, message='points are not enough')
            current_user.points -= pt
            log = PointLog(action, pt, user, issue)
            voter = Voter(user, issue)
            db.session.add(voter)
            db.session.add(log)
            issue.points += pt
        elif voter.value != value:
            voter.value = value
        else:
            return voter
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return abort(500, message='operation failed')
        return voter

api.add_resource(Issues, '/api/issues', endpoint='api.issues')
api.add_resource(IssueVoters, '/api/issues/<string:issue_id>'
                              '/voters/<string:username>',
                              endpoint='api.issue_voters')
