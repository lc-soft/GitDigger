from app import app
from flask import render_template
import flask_login

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
@flask_login.login_required
def dashboard():
    return 'Logged in as: ' + flask_login.current_user.id
