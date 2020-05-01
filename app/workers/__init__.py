from celery import Celery

worker = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
worker.conf.update(app.config)

import issue_worker
import user_worker
