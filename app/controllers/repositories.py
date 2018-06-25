from app import app, db, login_manager
from app.models.repository import Repository
from app.helpers.github_helper import GitHubHelper
from app.helpers.repositories_helper import RepositoriesHelper
from app.helpers.application_helper import flash
from app.services import users_service, issues_service, topics_service
from flask import request, redirect, abort, Blueprint, url_for, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm as Form
from wtforms import SelectField, StringField, validators
import requests

repos = Blueprint('repos', __name__)
repos_helper = RepositoriesHelper(repos)
github_helper = GitHubHelper(app)

def valid_github_repo_url(form, field):
    url = field.data
    host = '//github.com/'
    i = url.find(host)
    if i > 1 and len(url) > 24:
        nodes = url[i + len(host):].split('/')
        if len(nodes) == 2:
            return
    raise validators.ValidationError('Field must be a GitHub repository url.')

class RepositoryForm(Form):
    html_url = StringField('Repository url', [
        validators.InputRequired(),
        valid_github_repo_url
    ])

def create(data):
    name = data['full_name'].split('/')[1]
    user = users_service.get(data['owner']['id'])
    if user is None:
        user = users_service.create(data['owner'])
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Repository creation failed, '
                'we cannot import owner data', 'danger')
            return None
    else:
        repo = Repository.query.filter_by(
            owner_id=user.id,
            name=name
        ).first()
        if repo is not None:
            flash('Repository already exists', 'warning')
            return None
    try:
        repo = Repository(user, data)
        repo.imported_from = 'GitHub'
        db.session.add(repo)
        db.session.commit()
        flash('Repository created successfully')
    except Exception as e:
        db.session.rollback()
        flash('Repository creation failed', 'danger')
        return None
    try:
        for topic in repo.topics:
            topics_service.update_repos_count(topic)
        db.session.commit()
    except:
        db.session.rollback()
    return repo

@repos_helper.route('/', methods=['GET'])
def show(ctx):
    return ctx.render('show.html')

def delete(ctx):
    try:
        ctx.repo.topics = []
        db.session.delete(ctx.repo)
        db.session.commit()
        flash('Repository deleted successfully')
        return redirect(url_for('index'))
    except:
        db.session.rollback()
        flash('Repository deletion failed', 'danger')
        ctx.render('settings/index.html')

def handle_form_for_self(form, repos):
    if not form.validate_on_submit():
        return None
    full_name = form.full_name.data
    if repos is not None:
        for repo in repos:
            if repo['full_name'] == full_name:
                repo = create(repo)
                break
        else:
            flash('Repository does not exist', 'warning')
            return None
    return repo

@repos_helper.route('/settings', methods=['GET', 'POST'])
@login_required
def settings(ctx):
    action = request.form.get('action')
    if request.method == 'POST' and action == 'delete':
        return delete(ctx)
    return ctx.render('settings/index.html')

@repos_helper.route('/settings/github', methods=['GET', 'POST'])
@login_required
def github(ctx):
    return ctx.render('settings/github.html')

@github_helper.access_token_getter
def token_getter():
    if current_user is not None:
        return current_user.github_token

@repos.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    host = '//github.com/'
    form = RepositoryForm(request.form)
    source = request.form.get('source', 'self')
    if request.method == 'POST' and form.validate_on_submit():
        url = form.html_url.data
        repo_name = url[url.find(host) + len(host):]
        repo = github_helper.get_public_repo(repo_name)
        repo = create(repo)
    return render_template('repositories/new.html',
                            source=source,
                            form=form)

app.register_blueprint(repos)
