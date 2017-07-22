from app import app, login_manager
from flask import render_template
import flask_login

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
@flask_login.login_required
def settings():
    pass
