from app import app
from app.models.user import User
from app.models.repository import Repository
from werkzeug.contrib.cache import SimpleCache
from flask import abort, render_template
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
    
    def get_repo(self, username, name):
        user = User.query.filter_by(username=username).first()
        if user is None:
            return None
        repo = Repository.query.filter_by(owner_id=user.id, name=name).first()
        if repo is None:
            return None
        return repo

    def get_repo_by_id(self, origin_id, imported_from='GitHub'):
        return Repository.query.filter_by(
            origin_id=origin_id,
            imported_from=imported_from
        ).first()

    def route(self, rule, **options):
        app = self.app
        url_map = self.url_map
        get_repo = self.get_repo
        url_map[URL_PREFIX + rule] = True

        def decorator(func):
            @app.route(URL_PREFIX + rule, **options)
            @wraps(func)
            def wrapper(username, name, *args, **kw):
                repo = get_repo(username, name)
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
