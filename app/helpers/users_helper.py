from config import site
from random import random
from app.models.user import User
from werkzeug.security import generate_password_hash

class UsersHelper(object):
    def __init__(self, app):
        self.app = app

    def get_user(self, github_id):
        return User.query.filter_by(github_id=github_id).first()

    def create_user(self, data):
        pw = generate_password_hash(str(random()))
        email = 'github_%s@%s' % (data['login'], site.config['domain'])
        user = User(data['login'], email, pw, data['name'])
        user.github_id = data['id']
        user.github_username = data['login']
        user.avatar_url = data['avatar_url']
        user.owner = 'system'
        user.bio = data['bio']
        return user
