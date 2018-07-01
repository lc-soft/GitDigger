from app import db
from app.models.snippet import Snippet
from datetime import datetime

def update(s, data):
    s.file = data['file']
    s.line = data['line']
    s.language = data['language']
    s.content = data['content']
    s.content_start_line = data['content_start_line']
    s.content_end_line = data['content_end_line']
    s.description = data['description']
    s.commit_id = data['commit_id']
    s.updated_at = datetime.utcnow()
    return s

def find(repo_id):
    return Snippet.query.filter(Snippet.repository_id==repo_id)
