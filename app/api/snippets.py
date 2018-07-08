from app import db
from app.api import api
from app.api.auth import auth_required
from app.api.resource_fields import snippet_fields, voter_fields
from app.models.voter import Voter
from app.models.snippet import Snippet
from app.models.point_log import PointLog
from app.services import users_service, snippets_service, \
    voters_service, repositories_service as repos_service
from flask_restful import Resource, marshal, abort, reqparse
from flask_login import current_user
from flask import request
from sqlalchemy import func
from config import points

class Snippets(Resource):
    @auth_required
    def put(self, username, repo):
        picked_snippets = []
        snippets = request.get_json()
        if snippets is None:
            return abort(400, message='invalid data')
        repo = repos_service.get(username, repo)
        if repo is None:
            return abort(400, message='repository not found')
        for s in snippets_service.find(repo.id).all():
            filtered_snippets = []
            for snippet in snippets:
                if s.file != snippet['file'] \
                or s.commit_id == snippet['commit_id']:
                    filtered_snippets.append(snippet)
                    picked_snippets.append(s)
                    continue
                if s.description == snippet['description']:
                    snippets_service.update(s, snippet)
                    picked_snippets.append(s)
                    db.session.add(s)
                    break
            else:
                s.state = 'closed'
                db.session.add(s)
            snippets = filtered_snippets
        for snippet in snippets:
            s = Snippet(repo, snippet)
            picked_snippets.append(s)
            db.session.add(s)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return abort(500, message='snippets update failed')
        return [marshal(s, snippet_fields) for s in picked_snippets]

class SnippetVoters(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rating', type=int, required=True)

    def put(self, id, username):
        pt =  points.SNIPPET_RATING
        args = self.parser.parse_args()
        rating = args['rating']
        s = Snippet.query.get(id)
        if s is None:
            return abort(400, message='invalid id')
        user = users_service.get_by_username(username)
        if user is None:
            return abort(400, message='invalid username')
        rating_sum = snippets_service.get_rating_sum(s)
        voter = voters_service.get(user, s)
        if voter is None:
            if current_user.points - pt < 0:
                return abort(403, message='points are not enough')
            current_user.points -= pt
            s.ratings_count += 1
            s.rating = (rating_sum + rating) / s.ratings_count
            log = PointLog('SNIPPET_RATING', pt, user, s)
            voter = Voter(user, s)
            voter.value = rating
            db.session.add(voter)
            db.session.add(log)
            db.session.add(s)
        else:
            s.rating = (rating_sum - voter.value + rating) / s.ratings_count
            voter.value = rating
            db.session.add(voter)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return abort(500, message='operation failed')
        result = marshal(voter, voter_fields)
        result['snippet'] = marshal(s, snippet_fields)
        return result

api.add_resource(
    Snippets,
    '/api/repos/<string:username>/<string:repo>/snippets',
    endpoint='api.snippets'
)
api.add_resource(
    SnippetVoters,
    '/api/snippets/<string:id>/voters/<string:username>',
    endpoint='api.snippet_voters'
)
