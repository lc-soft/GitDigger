from app import worker, db, app
from app.models.task import Task
from app.models.user import User
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
import requests

logger = get_task_logger(__name__)

def get_profile(username):
    url = 'https://api.github.com/users/%s' % username
    try:
        result = requests.get(url, timeout=10)
        return result.json()
    except:
        return None

@worker.task
def update_profile():
    now = datetime.now()
    name = 'update_user_profile'
    task = Task.query.filter_by(target_type='system', name=name).first()
    if task is None:
        task = Task(name, None)
        db.session.add(task)
    time = datetime.now() - timedelta(days=30)
    query = User.query.order_by(User.last_login_reward_at.desc())
    query = query.filter(User.github_username.isnot(None))
    query = query.filter(User.last_login_reward_at > time)
    task.start(query.count())
    logger.info('total users: %d', task.total)
    while task.current < task.total:
        for user in query.limit(32).offset(task.current).all():
            data = get_profile(user.github_username)
            logger.info('update: %s, %s', user.github_username, 'done' if data else 'fail')
            if data is None:
                continue
            user.type = data['type']
            user.location = data['location']
            user.avatar_url = data['avatar_url']
            user.followers_count = data['followers']
            user.public_repos_count = data['public_repos']
        task.current += 32
        task.update()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            break
    task.finish()
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True
