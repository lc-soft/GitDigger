from app import app, db, login_manager
from app.models.topic import Topic
from app.models.issue import Issue
from app.models.voter import Voter
from app.models.user import User
from flask import render_template, request
from flask_login import current_user

@app.route('/')
def index():
    topics = Topic.query.order_by(
        Topic.group.desc(),
        Topic.issues_count.desc()
    ).limit(10).all()
    sort = request.args.get('sort', 'top')
    user_id = current_user.id if current_user.is_authenticated else 0
    terms = db.and_(Voter.target_id==Issue.id, Voter.user_id==user_id)
    case = db.case([(Voter.user_id==user_id, True)], else_=False)
    query = db.session.query(Issue, case.label('has_voted'))
    if sort == 'top':
        query = query.order_by(Issue.score.desc(), Issue.created_at.desc())
    else:
        query = query.order_by(Issue.created_at.desc())
    query = query.outerjoin(Voter, terms)
    feeds = query.all()
    ctx = {
        'feeds': feeds,
        'topics': topics,
        'navbar_active': 'stories',
        'feeds_sort_active': sort
    }
    return render_template('index.html', **ctx)
