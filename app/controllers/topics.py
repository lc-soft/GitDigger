from app import app, db
from app.models.topic import Topic
from app.models.user import topics as UserTopics
from flask import request, redirect, flash
from flask import Blueprint, url_for, render_template
from flask_login import current_user

topics = Blueprint('topics', __name__)

@topics.route('/topics', methods=['GET'])
def index():
    group, groups = [], []
    user_id = current_user.id if current_user.is_authenticated else 0
    terms = db.and_(UserTopics.c.user_id==user_id, UserTopics.c.topic_id==Topic.id)
    case = db.case([(UserTopics.c.user_id==user_id, True)], else_=False)
    query = db.session.query(Topic, case.label('has_following'))
    query = query.outerjoin(UserTopics, terms)
    topics = query.order_by(
        Topic.issues_count.desc(),
        Topic.followers_count.desc()
    ).limit(36).all()
    for t in topics:
        group.append(t)
        if len(group) >= 3:
            groups.append(group)
            group = []
    if len(group) > 0:
        groups.append(group)
    return render_template('topics/index.html',
                            groups=groups, navbar_active='topics')

@topics.route('/topics/<string:name>', methods=['GET'])
def show(name):
    return name

app.register_blueprint(topics)
