from lib import highlight, markdown

def init_app(app):
    app.add_template_filter(highlight.render, 'highlight')
    app.add_template_filter(markdown.render, 'markdown')