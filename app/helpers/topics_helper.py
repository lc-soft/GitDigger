from app import db
from app.models import issue
from app.models import repository
from app.models.topic import Topic

class TopicsHelper:
    def update_issues_count(self, topic):
        query = db.session.query(issue.topics)
        topic.issues_count = query.filter_by(topic_id=topic.id).count()
        return topic.issues_count

    def update_repos_count(self, topic):
        query = db.session.query(repository.topics)
        topic.repositories_count = query.filter_by(topic_id=topic.id).count()
        return topic.repositories_count
