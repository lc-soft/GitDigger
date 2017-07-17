from app import app
from config import github
from app.models.user import User
from flask import jsonify, request, redirect, url_for, Blueprint, render_template
from flask_github import GitHub

users = Blueprint('users', __name__)

# setup github-flask
app.config['GITHUB_CLIENT_ID'] = github.config['id']
app.config['GITHUB_CLIENT_SECRET'] = github.config['secret']
github = GitHub(app)

@users.route('/<string:username>', methods=['GET'])
def get(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(status=0, user=user)
    return jsonify(status=404)

@users.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    return 'join'

@users.route('/login')
def login():
    return render_template('login.html')

@users.route('/auth/github')
def auth_github():
    return github.authorize()

@users.route('/user')
def user():
    return str(github.get('user'))

@users.route('/api/authorizations/github')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)
    print access_token
    return redirect(next_url)

app.register_blueprint(users)
