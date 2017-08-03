from app import app, login_manager
from app.models.topic import Topic
from app.models.issue import Issue
from flask import render_template

@app.route('/')
def index():
    topics = Topic.query.limit(20).all()
    issues = Issue.query.all()
    ctx = {
        'navbar_active': 'stories',
        'secondary_navbar_active': 'top'
    }
    return render_template('index.html', topics=topics, issues=issues, **ctx)
