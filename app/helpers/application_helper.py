import flask
from app import app
from datetime import datetime
from flask import request, url_for
from flask_login import current_user

def flash(message, category='info'):
    return flask.flash(message, category)

@app.template_global()
def app_data():
    data = {
        'endpoint': request.endpoint,
        'api': {
            'issues': url_for('api.issues'),
            'snippet_voters': url_for('api.snippet_voters', id=':id', username=':username'),
        }
    }
    if current_user.is_authenticated:
        data['user'] = {
            'login': current_user.username,
            'name': current_user.name,
            'github_username': current_user.github_username
        }
    else:
        data['user'] = {
            'login': None,
            'name': 'unknown'
        }
    return data

@app.template_global()
def rating_options():
    return [
        (0, 0, 'so easy'),
        (2, 4, 'easy'),
        (4, 6, 'normal'),
        (6, 8, 'difficult'),
        (8, 10, 'so difficult')
    ]

@app.template_global()
def rating_text_tag(rating):
    level = 0
    options = rating_options()
    text = options[0][2]
    for i in range(len(options) - 1, 0, -1):
        if rating > options[i][0]:
            level = i
            text = options[i][2]
            break
    html = '<span class="rating-text js-rating-text" data-value="{0}">{1}</span>'
    return flask.Markup(html.format(level, text))

@app.template_global()
def timeago_tag(time, class_=''):
    html = '<time class="timeago {0}" datetime="{1}" title="{1}">{2}</time>'
    return flask.Markup(html.format(class_, time.isoformat(), time.ctime()))

@app.template_global()
def human_number(num):
    if num > 999:
        return ('%.1f' % (num / 1000.0)).rstrip('0').rstrip('.') + 'k'
    return num

@app.template_global()
def get_copyright_year():
    return datetime.now().year

@app.template_global()
def get_body_class():
    body_class = '-'.join(['page'] + flask.request.endpoint.split('.'))
    if current_user.is_authenticated:
        body_class = body_class + ' logged-in'
    return body_class

@app.template_global()
def url_for_vote(target):
    if not current_user.is_authenticated:
        return ''
    if target.__tablename__ == 'issue':
        return flask.url_for('api.issue_voters', issue_id=target.id,
                            username=current_user.username)
    return ''
