from app import app
from app.models.topic import Topic
from flask import request, redirect, flash
from flask import Blueprint, url_for, render_template

topics = Blueprint('topics', __name__)

@topics.route('/topics', methods=['GET'])
def index():
    group, groups = [], []
    topics = Topic.query.order_by(Topic.issues_count.desc()).limit(36).all()
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
