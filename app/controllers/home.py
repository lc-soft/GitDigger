from app import app, login_manager
from app.models.topic import Topic
from flask import render_template

@app.route('/')
def index():
    topics = Topic.query.limit(20).all()
    return render_template('index.html', topics=topics)
