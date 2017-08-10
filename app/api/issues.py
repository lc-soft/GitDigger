from app import db, csrf
from app.models.voter import Voter
from app.models.point_log import PointLog
from app.api import api, resource_fields
from app.services import users_service, issues_service, voters_service
from flask_restful import Resource, marshal_with, abort, reqparse
from flask_login import current_user
from config import points

class IssueVoters(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('action')

    @marshal_with(resource_fields.voter_fields)
    def put(self, issue_id, username):
        if not current_user.is_authenticated:
            return abort(401, message='permission denied')
        issue = issues_service.get(issue_id)
        if issue is None:
            return abort(400, message='issue not found')
        user = users_service.get_by_username(username)
        if user is None:
            return abort(400, message='user not found')
        args = self.parser.parse_args()
        action = args.get('action', 'upvote')
        value = -1 if action == 'downvote' else 1
        voter = voters_service.get(user, issue)
        if voter is None:
            if current_user.points < points.VOTE:
                return abort(403, message='points are not enough')
            log = PointLog(action, points.VOTE, user, issue)
            voter = Voter(user, issue)
            db.session.add(voter)
            db.session.add(log)
            issue.points += value
        elif voter.value != value:
            issue.points += value
            voter.value = value
        else:
            return voter
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return abort(500, message='operation failed')
        return voter

api.add_resource(IssueVoters, '/api/issues/<string:issue_id>'
                              '/voters/<string:username>',
                              endpoint='api.issue_voters')
