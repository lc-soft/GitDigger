from app import app

@app.template_global()
def snippet_file_link(s):
    return '{0}/blob/{1}/{2}#L{3}-L{4}'.format(
        s.repository.html_url, s.commit_id, s.file, 
        s.line, s.content_start_line
    )
