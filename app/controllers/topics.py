from app import app, db
from app.models.topic import Topic
from app.models.voter import Voter
from app.models.issue import Issue
from app.models.user import topics as UserTopics
from app.services import topics_service
from flask import request, redirect, flash, abort
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
    has_following = False
    topic = topics_service.get(name)
    if topic is None:
        return abort(404)
    page = int(request.args.get('page', 1))
    sort = request.args.get('sort', 'top')
    target = request.args.get('target', 1)
    if current_user.is_authenticated:
        user_id = current_user.id
        for t in current_user.following_topics:
            if t.name == topic.name:
                has_following = True
                break
    else:
        user_id = 0
    terms = db.and_(Voter.target_id==Issue.id, Voter.user_id==user_id)
    case = db.case([(Voter.user_id==user_id, True)], else_=False)
    query = db.session.query(Issue, case.label('has_voted'))
    query = query.filter(Issue.topics.any(Topic.name==topic.name))
    if sort == 'top':
        query = query.order_by(Issue.score.desc(), Issue.created_at.desc())
    else:
        query = query.order_by(Issue.created_at.desc())
    query = query.outerjoin(Voter, terms)
    feeds = query.paginate(page, 15)
    ctx = {
        'feeds': feeds,
        'topic': topic,
        'sort': sort,
        'navbar_active': 'topics',
        'has_following': has_following
    }
    if target == '#topic-feeds':
        return render_template('components/_feed_list.html', **ctx)
    return render_template('topics/show.html', **ctx)

app.register_blueprint(topics)
