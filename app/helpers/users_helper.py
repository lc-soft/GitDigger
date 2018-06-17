import avinit
from app import app
from flask import Markup

class UsersHelper(object):
    def __init__(self, app):
        self.app = app

@app.template_global()
def user_avatar_tag(user):
    avatar_url = user.avatar_url
    if not user.avatar_url:
        avatar_url = avinit.get_avatar_data_url(user.name)
    return Markup('<img class="user-avatar" title="%s" alt="%s" src="%s">' %
                   (user.username, user.username, avatar_url))

@app.template_global()
def user_is_following_topic(user, topic_name):
    if user.is_authenticated:
        for topic in user.following_topics:
            if topic.name == topic_name:
                return True
    return False
