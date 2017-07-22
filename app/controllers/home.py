from app import app, login_manager
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')
