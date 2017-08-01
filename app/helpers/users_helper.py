from app import app
from flask import Markup

class UsersHelper(object):
    def __init__(self, app):
        self.app = app

@app.template_global()
def user_avatar_tag(user):
    return  Markup('<img class="user-avatar" alt="%s" src="%s">' %
                   (user.username, user.avatar_url))
