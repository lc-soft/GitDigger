from app import app
from datetime import datetime
from config.site import config
from app.models.repository import Repository
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

def get_repos_count():
    count = cache.get('repos_count')
    if count is not None:
        return count
    count = Repository.query.count()
    cache.set('repos_count', count, 600)
    return count

def get_copyright_year():
    return datetime.now().year

@app.context_processor
def site_global_data():
    return dict(get_repos_count=get_repos_count, 
                get_copyright_year=get_copyright_year,
                **config)
