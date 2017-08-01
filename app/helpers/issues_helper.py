from app import app

@app.template_global()
def issue_main_topics(issue):
    topics = sorted(issue.topics, key=lambda t: t.repositories_count)
    topics = sorted(topics, key=lambda t: t.group != 'language')
    return topics[:3]
