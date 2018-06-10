import flask
from app import app
from datetime import datetime
from flask_login import current_user

def flash(message, category='info'):
    flask.flash(message, category)

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
def feed_icon(feed):
    label_class = 'label'
    icon_class = 'octicon'
    if feed.state == 'open':
        icon_class += ' octicon-issue-opened'
        label_class += ' label-green'
    else:
        icon_class += ' octicon-issue-closed'
        label_class += ' label-red'
    return flask.Markup('''<span class="%s">
      <i class="%s"></i>
    </span>''' % (label_class, icon_class))

@app.template_global()
def url_for_vote(target):
    if not current_user.is_authenticated:
        return ''
    if target.__tablename__ == 'issue':
        return flask.url_for('api.issue_voters', issue_id=target.id,
                            username=current_user.username)
    return ''

@app.template_filter()
def timesince(dt, default='just now'):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds')
    )
    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default
