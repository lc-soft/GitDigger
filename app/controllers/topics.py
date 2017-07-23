from app import app
from app.models.topic import Topic
from flask import request, redirect, flash
from flask import Blueprint, url_for, render_template

topics = Blueprint('topics', __name__)

@topics.route('/topics', methods=['GET'])
def index():
    topics = Topic.query.all()
    return render_template('topics/index.html', topics=topics)

@topics.route('/topics/<string:name>', methods=['GET'])
def show(name):
    return name

app.register_blueprint(topics)
