from app import app, db, login_manager
from app.models.user import User
from app.models.repository import Repository
from app.helpers.application_helper import flash
from app.helpers.github_helper import GitHubHelper
from app.helpers.topics_helper import TopicsHelper
from app.helpers.repositories_helper import RepositoriesHelper
from flask import request, redirect, abort
from flask import Blueprint, url_for, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm as Form
from wtforms import SelectField, validators

repos = Blueprint('repos', __name__)
repos_helper = RepositoriesHelper(repos)
github_helper = GitHubHelper(app)
topics_helper = TopicsHelper()

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
            topics_helper.update_repos_count(topic)
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

@repos_helper.route('/settings', methods=['GET', 'POST'])
@login_required
def settings(ctx):
    action = request.form.get('action')
    if request.method == 'POST' and action == 'delete':
        return delete(ctx)
    return ctx.render('settings/index.html')

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
