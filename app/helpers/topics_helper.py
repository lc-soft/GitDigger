from app import app
from config.lang_colors import colors

@app.template_global()
def topic_color_style(topic):
    if topic.group == 'language':
        color = colors.get(topic.name)
        if color is not None:
            return 'color: #fff; background-color: %s;' % color
    return ''

@app.template_global()
def topics_sorted(topics):
    topics = sorted(topics, key=lambda t: t.repositories_count)
    return sorted(topics, key=lambda t: t.group != 'language')

@app.template_global()
def url_for_topic(topic):
    return ''
