from app import db, login_manager
from app.api import api
from app.api.auth import auth_required
from app.api.resource_fields import snippet_fields
from app.models.snippet import Snippet
from app.services import users_service, snippets_service, \
    repositories_service as repos_service
from flask_restful import Resource, marshal, abort
from flask import request

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
                db.session.delete(s)
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

api.add_resource(Snippets, '/api/repos/<string:username>/<string:repo>/snippets', endpoint='api.snippets')
