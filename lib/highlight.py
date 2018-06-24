from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def render(code, lang, linenostart):
    lexer = get_lexer_by_name(lang, stripall=True)
    formater = HtmlFormatter(
        linenos='table',
        linenostart=linenostart
    )
    return highlight(code, lexer, formater)
