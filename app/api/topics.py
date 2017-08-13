from app import db
from app.api import api, resource_fields
from app.services import topics_service
from flask_restful import Resource, marshal_with, abort, reqparse
from flask_login import current_user

class UserTopics(Resource):
    @marshal_with(resource_fields.topic_fields)
    def post(self, name):
        if not current_user.is_authenticated:
            return abort(401, message='permission denied')
        for topic in current_user.following_topics:
            if topic.name == name:
                return topic
        topic = topics_service.get(name)
        if topic is None:
            return abort(400, message='topic not found')
        try:
            current_user.following_topics.append(topic)
            topic.followers_count += 1
            print topic.followers_count
            db.session.commit()
        except:
            db.session.rollback()
            return abort(500, message='operation failed')
        return topic

    def delete(self, name):
        topic = None
        if not current_user.is_authenticated:
            return abort(401, message='permission denied')
        for topic in current_user.following_topics:
            if topic.name == name:
                break
        else:
            return abort(400, message='topic not found')
        try:
            current_user.following_topics.remove(topic)
            if topic.followers_count > 0:
                topic.followers_count -= 1
            db.session.commit()
        except:
            db.session.rollback()
            return abort(500, message='operation failed')

api.add_resource(UserTopics, '/api/user/topics/<string:name>',
                              endpoint='api.user_topics')
