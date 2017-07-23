from config import github
from app.helpers.github import github
from app.models.repository import Repository
from app import app, db, login_manager
from flask import request, redirect, flash
from flask import Blueprint, url_for, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm as Form
from wtforms import SelectField, validators

repos = Blueprint('repos', __name__)

class RepositoryForm(Form):
    full_name = SelectField('Repository')

def create(data):
    repo = Repository.query.filter_by(owner_id=current_user.id).first()
    if repo is not None:
        flash('Repository already exists')
        return
    repo = Repository(current_user.id, data)
    db.session.add(repo)
    db.session.commit()
    flash('Repository created successfully')

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
