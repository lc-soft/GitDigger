from functools import wraps
from flask import request
from flask_restful import abort
from app.models.user import User
from werkzeug.security import check_password_hash

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return abort(401)
        login = auth.username
        if login[1:-1].find('@') >= 0:
            user = User.query.filter_by(email=login).first()
            login_type = 'email'
        else:
            user = User.query.filter_by(username=login).first()
            login_type = 'username'
        if user is None:
            return abort(401, message='Unknown %s' % login_type)
        if not check_password_hash(user.password, auth.password):
            return abort(401, message='Invalid password')
        return f(*args, **kwargs)
    return decorated
