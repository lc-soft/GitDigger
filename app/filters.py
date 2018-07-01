from lib import highlight, markdown

def autoheader(content):
    lines = content.split('\n')
    if len(lines) > 1:
        header = lines[0].strip()
        if len(header) < 78 and ',.!?~+-'.find(header[-1]) < 0:
            lines[0] = '<div class="header">{}</div>'.format(header)
            return '\n'.join(lines)
    return content

def init_app(app):
    app.add_template_filter(autoheader, 'autoheader')
    app.add_template_filter(highlight.render, 'highlight')
    app.add_template_filter(markdown.render, 'markdown')