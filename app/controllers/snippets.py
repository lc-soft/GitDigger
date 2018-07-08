from app import app, db
from app.models.snippet import Snippet
from app.models.repository import Repository
from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user
from datetime import datetime

view = Blueprint('snippets', __name__)

@view.route('/fixme')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    snippets = Snippet.query.order_by(Snippet.updated_at.desc())
    return render_template(
        'snippets/index.html',
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
