from app import app, db
from app.models.snippet import Snippet
from app.models.repository import Repository
from flask import Blueprint, render_template, request
from flask_login import current_user
from datetime import datetime

view = Blueprint('snippets', __name__)

@view.route('/fixme')
def index():
    snippets = Snippet.query.all()
    return render_template('snippets/index.html', snippets=snippets, navbar_active='fixme')

app.register_blueprint(view)
