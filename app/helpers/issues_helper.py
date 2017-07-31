from app import app

@app.template_global()
def issue_main_topics(issue):
    topics = []
    for topic in issue.topics:
        if topic.group == 'language':
            topics.insert(0, topic)
        else:
            topics.append(topic)
    return topics[:4]
