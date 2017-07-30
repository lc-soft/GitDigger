from github_webhook import Webhook

class WebhookService(Webhook):
    def __init__(self, app):
        url = app.config.get('GITHUB_WEBHOOK_URL', '/api/webhook')
        secret = app.config.get('GITHUB_WEBHOOK_SECRET')
        Webhook.__init__(self, app, url, secret)
