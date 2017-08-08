from app import app, login_manager
from app.models.topic import Topic
from app.models.issue import Issue
from flask import render_template

@app.route('/')
def index():
    topics = Topic.query.order_by(
        Topic.group.desc(),
        Topic.issues_count.desc()
    ).limit(10).all()
    feeds = Issue.query.order_by('score DESC').all()
    ctx = {
        'navbar_active': 'stories',
        'feeds_sort_active': 'top'
    }
    return render_template('index.html', topics=topics, feeds=feeds, **ctx)
