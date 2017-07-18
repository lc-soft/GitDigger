from config import github
from app import app, login_manager
from app.models.user import User
import flask, flask_login, flask_github

users = flask.Blueprint('users', __name__)

# setup github-flask
app.config['GITHUB_CLIENT_ID'] = github.config['id']
app.config['GITHUB_CLIENT_SECRET'] = github.config['secret']
github = flask_github.GitHub(app)

@users.route('/<string:username>', methods=['GET'])
def get(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return flask.jsonify(status=0, user=user)
    return flask.jsonify(status=404)

@users.route('/join', methods=['GET', 'POST'])
def join():
    if flask.request.method == 'GET':
        return flask.render_template('join.html')
    return 'join'

@users.route('/login')
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    user = flask.request.form.get('user')
    login = user['login']
    password = user['password']
    if login[1:-1].find('@') >= 0:
        user = User.query.filter_by(email=login, password=password).first()
    else:
        user = User.query.filter_by(username=login, password=password).first()
    if user is None:
        return flask.redirect(flask.url_for('users.login'))
    flask_login.login_user(user)
    flask.flash('Logged in successfully.')
    next = flask.request.args.get('next')
    return flask.redirect(next or flask.url_for('home.dashboard'))

@users.route('/auth/github')
def auth_github():
    return github.authorize()

@users.route('/user')
def user():
    return str(github.get('user'))

@users.route('/api/authorizations/github')
@github.authorized_handler
def authorized(access_token):
    next_url = flask.request.args.get('next') or flask.url_for('index')
    if access_token is None:
        return flask.redirect(next_url)
    print access_token
    return flask.redirect(next_url)

app.register_blueprint(users)
