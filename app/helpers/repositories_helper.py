from app import app
from app.models.repository import Repository
from app.services import repositories_service as repos_service
from werkzeug.contrib.cache import SimpleCache
from flask import abort, render_template, Markup
from functools import wraps

cache = SimpleCache()

URL_PREFIX = '/<string:username>/<string:name>'
TEMPLATE_PREFIX = 'repositories/'

class RepositoryContext:
    def __init__(self, url_map, repo):
        self.repo = repo
        self.params = {}
        for url in url_map:
            i = url.find(URL_PREFIX)
            if i != 0:
                continue
            name = 'url_for_repo%s' % url[len(URL_PREFIX):].replace('/', '_')
            url = url.replace('<string:username>', repo.owner.username)
            url = url.replace('<string:name>', repo.name)
            self.params[name] = url
        self.params['repo'] = repo

    def render(self, path, **options):
        kwargs = dict(self.params, **options)
        return render_template(TEMPLATE_PREFIX + path, **kwargs)

class RepositoriesHelper:
    def __init__(self, app):
        self.app = app
        self.url_map = {}
    
    def route(self, rule, **options):
        app = self.app
        url_map = self.url_map
        url_map[URL_PREFIX + rule] = True

        def decorator(func):
            @app.route(URL_PREFIX + rule, **options)
            @wraps(func)
            def wrapper(username, name, *args, **kw):
                repo = repos_service.get(username, name)
                if repo is None:
                    return abort(404)
                ctx = RepositoryContext(url_map, repo)
                return func(ctx, *args, **kw)
            return wrapper
        return decorator

@app.template_global()
def get_repos_count():
    count = cache.get('repos_count')
    if count is not None:
        return count
    count = Repository.query.count()
    cache.set('repos_count', count, 600)
    return count

class UsersHelper(object):
    def __init__(self, app):
        self.app = app

@app.template_global()
def repo_logo_tag(repo):
    url = repo.logo_url
    if not url:
        url = repo.owner.avatar_url
    return  Markup('<img class="repo-logo" title="%s" alt="%s" src="%s">' %
                   (repo.name, repo.name, url))
