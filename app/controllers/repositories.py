from app import app, db, login_manager
from app.models.user import User
from app.models.repository import Repository
from app.helpers.github import github
from flask import request, redirect, flash, abort
from flask import Blueprint, url_for, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm as Form
from wtforms import SelectField, validators

repos = Blueprint('repos', __name__)
repo_path = '/<string:username>/<string:name>'

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

def get_repo(username, name):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    repo = Repository.query.filter_by(owner_id=user.id, name=name).first()
    if repo is None:
        return None
    return repo

@repos.route(repo_path, methods=['GET'])
def show(username, name):
    repo = get_repo(username, name)
    if repo is None:
        return abort(404)
    return render_template('repositories/show.html', repo=repo)

@repos.route(repo_path + '/settings', methods=['GET'])
def settings(username, name):
    repo = get_repo(username, name)
    if repo is None:
        return abort(404)
    return render_template('repositories/settings/index.html', repo=repo)

@repos.route(repo_path + '/settings/github', methods=['GET'])
def repo_github(username, name):
    repo = get_repo(username, name)
    if repo is None:
        return abort(404)
    return render_template('repositories/settings/github.html', repo=repo)

@repos.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    choices = []
    repos = github.get_public_repos(True)
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
