from config import github
from config import database

def init_app(app):
    github.init_app(app)
    database.init_app(app)
    # setup secret key 
    app.config['SECRET_KEY'] = '[lc-soft.io, gitdigger.com]'
    # setup github-flask
    app.config['TEMPLATES_AUTO_RELOAD'] = True
