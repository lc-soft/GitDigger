from config import site
from random import random
from app.models.user import User
from werkzeug.security import generate_password_hash

def get(github_id):
    return User.query.filter_by(github_id=github_id).first()

def get_by_username(username):
    return User.query.filter_by(username=username).first()

def create(data):
    pw = generate_password_hash(str(random()))
    email = 'github_%s@%s' % (data['login'], site.config['domain'])
    user = User(data['login'], email, pw, data.get('name'))
    user.github_id = data['id']
    user.github_username = data['login']
    user.avatar_url = data['avatar_url']
    user.bio = data.get('bio', '')
    user.owner = 'system'
    return user
