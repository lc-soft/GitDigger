from app import app

@app.template_global()
def topics_sorted(topics):
    topics = sorted(topics, key=lambda t: t.repositories_count)
    return sorted(topics, key=lambda t: t.group != 'language')

@app.template_global()
def url_for_topic(topic):
    return ''
