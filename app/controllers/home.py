from app import app, db, login_manager
from app.models.topic import Topic
from app.models.issue import Issue
from app.models.voter import Voter
from app.models.user import User
from flask import render_template, request
from flask_login import current_user
from datetime import datetime, timedelta

@app.route('/')
def index():
    topic = None
    timeframe = None
    sort = request.args.get('sort', 'top')
    topic_name = request.args.get('topic')
    if current_user.is_authenticated:
        user_id = current_user.id
        topics = current_user.following_topics
    else:
        user_id = 0
        topics = Topic.query.order_by(
            Topic.group.desc(),
            Topic.issues_count.desc()
        ).limit(10).all()
    terms = db.and_(Voter.target_id==Issue.id, Voter.user_id==user_id)
    case = db.case([(Voter.user_id==user_id, True)], else_=False)
    query = db.session.query(Issue, case.label('has_voted'))
    if topic_name:
        if user_id > 0:
            for topic in current_user.following_topics:
                if topic.name == topic_name:
                    break
            else:
                topic = None
        else:
            topic = Topic.query.filter_by(name=topic_name).first()
    if topic:
        query = query.filter(Issue.topics.any(Topic.name==topic_name))
    elif user_id > 0 and len(current_user.following_topics) > 0:
        topic_terms = []
        for t in current_user.following_topics:
            topic_terms.append(Issue.topics.any(Topic.name==t.name))
        query = query.filter(db.or_(*topic_terms))
    if sort == 'top':
        days = {
            'today': 0,
            'week': 7,
            'month': 30,
            'year': 365
        }
        now = datetime.now()
        time = datetime(now.year, now.month, now.day)
        timeframe = request.args.get('timeframe')
        if days.get(timeframe) is None:
            timeframe = 'year'
        time -= timedelta(days=days[timeframe])
        query = query.filter(Issue.created_at > time)
        query = query.order_by(Issue.score.desc(), Issue.created_at.desc())
    else:
        query = query.order_by(Issue.created_at.desc())
    query = query.outerjoin(Voter, terms)
    feeds = query.all()
    ctx = {
        'feeds': feeds,
        'topics': topics,
        'timeframe': timeframe,
        'navbar_active': 'stories',
        'topic_name': topic_name,
        'topic': topic,
        'sort': sort
    }
    return render_template('index.html', **ctx)
