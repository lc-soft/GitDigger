from app import app, db
from app.models.topic import Topic
from app.models.snippet import Snippet
from app.models.repository import Repository
from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user
from datetime import datetime

view = Blueprint('snippets', __name__)

@view.route('/fixme')
@view.route('/fixme/language/<string:language>')
def index(language=None):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    snippets = Snippet.query.order_by(Snippet.updated_at.desc())\
        .filter(Snippet.state=='open')
    languages = Topic.query.filter(Topic.group=='language')\
        .order_by(Topic.snippets_count.desc()).limit(16).all()
    if language:
        snippets = snippets.filter(Snippet.language==language)
    return render_template(
        'snippets/index.html',
        languages=languages,
        language=language,
        pagination=Pagination(
            page=page,
            total=snippets.count(),
            bs_version=4,
            css_framework='bootstrap',
            alignment='center',
            record_name='snippets'
        ),
        snippets=snippets.paginate(page, 10),
        navbar_active='fixme'
    )

app.register_blueprint(view)
