from app import worker, db
from app.models.issue import Issue
from app.models.task import Task
from lib.ranking import get_score
from datetime import datetime
import time

@worker.task
def update_ranking_score():
    now = datetime.now()
    name = 'update_ranking_score'
    task = Task.query.filter_by(target_type='system', name=name).first()
    if task is None:
        task = Task(name, None)
        db.session.add(task)
    query = Issue.query.order_by('created_at')
    task.start(query.count())
    while task.current < task.total:
        print task.current, task.total
        for issue in query.limit(32).offset(task.current).all():
            hours = (now - issue.created_at).total_seconds() / 3600
            issue.score = get_score(issue.points, hours,
                                    issue.comments_count)
        task.current += 32
        task.update()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return
    task.finish()
    try:
        db.session.commit()
    except:
        db.session.rollback()
