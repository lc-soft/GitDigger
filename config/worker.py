from datetime import timedelta

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = {
    'update-issue-ranking-score': {
        'task': 'app.workers.issue_worker.update_ranking_score',
        'schedule': timedelta(minutes=10)
    }
}
