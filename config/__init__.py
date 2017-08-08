from config import github, database

def init_app(app):
    app.config.from_object(github)
    app.config.from_object(database)
    app.config['SECRET_KEY'] = '[lc-soft.io, gitdigger.com]'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
