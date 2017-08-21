from app import app, db, login_manager
from app.models.user import User
from app.models.repository import Repository
from app.helpers.github_helper import GitHubHelper
from app.helpers.repositories_helper import RepositoriesHelper
from app.helpers.application_helper import flash
from app.services import issues_service
from app.services import topics_service
from flask import request, redirect, abort
from flask import Blueprint, url_for, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm as Form
from wtforms import SelectField, validators
import requests

repos = Blueprint('repos', __name__)
repos_helper = RepositoriesHelper(repos)
github_helper = GitHubHelper(app)

class RepositoryForm(Form):
    full_name = SelectField('Repository')

def create(data):
    name = data['full_name'].split('/')[1]
    repo = Repository.query.filter_by(
        owner_id=current_user.id, 
        name=name
    ).first()
    if repo is not None:
        flash('Repository already exists', 'warning')
        return
    try:
        repo = Repository(current_user, data)
        repo.imported_from = 'GitHub'
        db.session.add(repo)
        db.session.commit()
        flash('Repository created successfully')
    except Exception as e:
        db.session.rollback()
        flash('Repository creation failed', 'danger')
        return
    try:
        for topic in repo.topics:
            topics_service.update_repos_count(topic)
        db.session.commit()
    except:
        db.session.rollback()

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

def import_issues(repo):
    count = 0
    params = { 'state': 'all', 'page': 1 }
    url = 'https://api.github.com/repos/%s/%s/issues'
    url = url %(repo.owner.github_username, repo.name)
    while True:
        try:
            result = requests.get(url, params=params, timeout=10)
        except:
            flash('Issues import failed', 'danger')
            return False
        issues = result.json()
        if len(issues) < 1:
            break
        for data in issues:
            if data.get('pull_request'):
                continue
            count += 1
            issue = issues_service.get_by_origin_id(data['id'])
            if issue is None:
                issue = issues_service.create(data, repo)
                if issue is None:
                    return False
                db.session.add(issue)
                continue
            issues_service.update(issue, data)
        params['page'] += 1
    try:
        db.session.commit()
        flash('%d issues imported successfully' % count, 'success')
    except:
        db.session.rollback()
        flash('Issues import failed', 'danger')
        return False
    return True

def import_pull_requests(repo):
    pass

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
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'import-issues':
            import_issues(ctx.repo)
        elif action == 'import-pulls':
            import_pull_requests(ctx.repo)
    return ctx.render('settings/github.html')

@github_helper.access_token_getter
def token_getter():
    if current_user is not None:
        return current_user.github_token

@repos.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    choices = []
    repos = github_helper.get_public_repos(current_user.github_username)
    if repos is None:
        return render_template('repositories/new.html', form=None)
    form = RepositoryForm(request.form)
    for repo in repos:
        full_name = repo['full_name']
        choices.append((full_name, full_name))
    form.full_name.choices = choices
    if request.method == 'POST' and form.validate_on_submit():
        full_name = form.full_name.data
        for repo in repos:
            if repo['full_name'] == full_name:
                create(repo)
                break
        else:
            flash('Repository does not exist', 'warning')
    return render_template('repositories/new.html', form=form)

app.register_blueprint(repos)
