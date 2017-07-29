from app import app, db
from github_webhook import Webhook

url = app.config.get('GITHUB_WEBHOOK_URL', '/api/webhook')
secret = app.config.get('GITHUB_WEBHOOK_SECRET')
webhook = Webhook(app, url, secret)

@webhook.hook()
def on_push(data):
    print data

@webhook.hook()
def on_issues(data):
    print data

@webhook.hook()
def on_issue_comment(data):
    print data

@webhook.hook()
def on_commit_comment(data):
    print data

@webhook.hook()
def on_pull_request_review(data):
    print data

@webhook.hook()
def on_pull_request_comment(data):
    print data

@webhook.hook()
def on_release(data):
    print data

@webhook.hook()
def on_repository(data):
    print data

@webhook.hook()
def on_create(data):
    print data

@webhook.hook()
def on_fork(data):
    print data

@webhook.hook()
def on_watch(data):
    print data

@webhook.hook()
def on_member(data):
    print data
