import flask

def flash(message, category='info'):
    flask.flash(message, category)
