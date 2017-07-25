from app import app, db, login_manager
from app.models.user import User
from app.models.repository import Repository
from app.helpers.github_helper import GitHubHelper
from app.helpers.repositories_helper import RepositoriesHelper
from flask import request, redirect, flash, abort
from flask import Blueprint, url_for, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm as Form
from wtforms import SelectField, validators

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
        flash('Repository already exists')
        return
    repo = Repository(current_user.id, data)
    db.session.add(repo)
    db.session.commit()
    flash('Repository created successfully')

@repos_helper.route('/', methods=['GET'])
def show(ctx):
    return ctx.render('show.html')

@repos_helper.route('/settings', methods=['GET'])
def settings(ctx):
    return ctx.render('settings/index.html')

@repos_helper.route('/settings/github', methods=['GET'])
def repo_github(ctx):
    return ctx.render('settings/github.html')

@github_helper.access_token_getter
def token_getter():
    if current_user is not None:
        return current_user.github_token

@repos.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    choices = []
    repos = github_helper.get_public_repos(True)
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
            flash('Repository does not exist')
    return render_template('repositories/new.html', form=form)

app.register_blueprint(repos)
