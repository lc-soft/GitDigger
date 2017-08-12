from app import app, db, login_manager
from app.models.topic import Topic
from app.models.issue import Issue
from app.models.voter import Voter
from app.models.user import User
from flask import render_template
from flask_login import current_user

@app.route('/')
def index():
    topics = Topic.query.order_by(
        Topic.group.desc(),
        Topic.issues_count.desc()
    ).limit(10).all()
    user_id = current_user.id if current_user.is_authenticated else 0
    terms = Voter.target_id==Issue.id and Voter.target_type=='issue'
    case = db.case([(Voter.user_id==user_id, True)], else_=False)
    query = db.session.query(Issue, case.label('has_voted'))
    feeds = query.outerjoin(Voter, terms).order_by(Issue.score.desc()).all()
    ctx = {
        'navbar_active': 'stories',
        'feeds_sort_active': 'top'
    }
    return render_template('index.html', topics=topics, feeds=feeds, **ctx)
