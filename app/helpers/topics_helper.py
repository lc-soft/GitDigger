from app import app
from config.lang_colors import colors

@app.template_global()
def topic_color_style(topic):
    if topic.group == 'language':
        color = colors.get(topic.name)
        if color is not None:
            return 'color: #fff; background-color: %s;' % color
    return ''
