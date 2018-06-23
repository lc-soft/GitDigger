from app import app, db, login_manager
from app.models.user import User
from app.models.task import Task
from app.models.topic import Topic
from app.models.issue import Issue
from app.models.voter import Voter
from app.models.repository import Repository
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from datetime import datetime, timedelta

dashboard_view = Blueprint('dashboard', __name__)

def recommend_users():
    time = datetime.now() - timedelta(days=365)
    query = User.query.order_by(User.last_login_reward_at.desc())
    query = query.filter(User.last_login_reward_at > time)
    query = query.filter(User.type == 'User')
    return query

def recommend_repos():
    return Repository.query.order_by(Repository.imported_at.desc())

def dashboard(sort='top', topic_name=None):
    days = {
        'today': 0,
        'week': 7,
        'month': 30,
        'year': 365
    }
    topic = None
    sidebar_active = sort
    user_id = current_user.id
    page = int(request.args.get('page', 1))
    target = request.args.get('target', 1)
    timeframe = request.args.get('timeframe')
    topics = current_user.following_topics
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
        sidebar_active = None
        query = query.filter(Issue.topics.any(Topic.name==topic_name))
    elif len(current_user.following_topics) > 0:
        topic_terms = []
        for t in current_user.following_topics:
            topic_terms.append(Issue.topics.any(Topic.name==t.name))
        query = query.filter(db.or_(*topic_terms))
    if sort == 'top':
        now = datetime.now()
        time = datetime(now.year, now.month, now.day)
        if days.get(timeframe) is None:
            timeframe = 'year'
        time -= timedelta(days=days[timeframe])
        query = query.filter(Issue.created_at > time)
        query = query.order_by(Issue.score.desc(), Issue.created_at.desc())
    else:
        query = query.order_by(Issue.created_at.desc())
    query = query.outerjoin(Voter, terms)
    feeds = query.paginate(page, 15)
    ctx = {
        'feeds': feeds,
        'topics': topics,
        'timeframe': timeframe,
        'sidebar_active': sidebar_active,
        'navbar_active': '',
        'topic_name': topic_name,
        'topic': topic
    }
    if target == '#feeds-container':
        return render_template('components/_feeds.html', **ctx)
    return render_template('dashboard/index.html', **ctx)

@dashboard_view.route('/recent')
@login_required
def recent():
    return dashboard('recent')

@dashboard_view.route('/pinned/<string:topic_name>')
@login_required
def pinned(topic_name):
    return dashboard('top', topic_name)

@app.route('/explore')
def explore():
    days = {
        'today': 0,
        'week': 7,
        'month': 30,
        'year': 365
    }
    user_id = 0
    navbar_active = 'home'
    page = int(request.args.get('page', 1))
    target = request.args.get('target', 1)
    timeframe = request.args.get('timeframe')
    users = recommend_users().limit(10).all()
    repos = recommend_repos().limit(6).all()
    topics = Topic.query.order_by(
        Topic.group.desc(),
        Topic.issues_count.desc()
    ).limit(10).all()
    if current_user.is_authenticated:
        user_id = current_user.id
        navbar_active = 'explore'
    terms = db.and_(Voter.target_id==Issue.id, Voter.user_id==user_id)
    case = db.case([(Voter.user_id==user_id, True)], else_=False)
    query = db.session.query(Issue, case.label('has_voted'))
    now = datetime.now()
    time = datetime(now.year, now.month, now.day)
    if days.get(timeframe) is None:
        timeframe = 'year'
    time -= timedelta(days=days[timeframe])
    query = query.filter(Issue.created_at > time)
    query = query.order_by(Issue.score.desc(), Issue.created_at.desc())
    query = query.outerjoin(Voter, terms)
    feeds = query.paginate(page, 10)
    ctx = {
        'feeds': feeds,
        'topics': topics,
        'users': users,
        'repos': repos,
        'timeframe': timeframe,
        'navbar_active': navbar_active
    }
    if target == '#feeds-container':
        return render_template('components/_feeds.html', **ctx)
    return render_template('home/index.html', **ctx)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return dashboard()
    return explore()

def users_status():
    q = User.query
    now = datetime.now()
    month_start = datetime(now.year, now.month, 1, 0)
    actual_users = q.filter(User.type == 'User').filter(User.owner == 'user')
    active_users = actual_users.filter(User.last_active_at > month_start)
    return {
        'count': q.count(),
        'actual_count': actual_users.count(),
        'active_count': active_users.count(),
        'new_count': q.filter(User.created_at > month_start).count()
    }

@app.route('/status')
def status():
    tasks = Task.query.order_by(Task.updated_at.desc()).all()
    ctx = {
        'navbar_active': 'status',
        'users': users_status(),
        'tasks': tasks
    }
    return render_template('home/status.html', **ctx)

app.register_blueprint(dashboard_view)
