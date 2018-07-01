import flask
from app import app
from datetime import datetime
from flask_login import current_user

def flash(message, category='info'):
    return flask.flash(message, category)

@app.template_global()
def rating_text_tag(rating):
    if rating > 8:
        level = 4
        text = 'so difficult'
    elif rating > 7:
        level = 3
        text = 'difficult'
    elif rating > 4:
        level = 2
        text = 'normal'
    elif rating > 2:
        level = 1
        text = 'easy'
    else:
        level = 0
        text = 'so easy'
    html = '<span class="rating-text rating-text-{0}">{1}</span>'
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
