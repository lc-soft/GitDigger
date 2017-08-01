from app import app
from webhook_service import WebhookService
import issues_service
import repositories_service

webhook = WebhookService(app)
