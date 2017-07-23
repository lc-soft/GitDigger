from app import app
import flask_github

class GitHub(flask_github.GitHub):
    cache = {}

    def get_user(self, cache=False):
        if cache:
            user = self.cache.get('user')
            if user is not None:
                return user
        try:
            user = self.get('user')
        except:
            user = None
        self.cache['user'] = user
        return user

    def get_public_repos(self, cache=False):
        repos = []
        if cache:
            repos = self.cache.get('public_repos')
            if repos is not None:
                return repos
        user = self.get_user(cache=True)
        if user is None:
            return None
        url = '%susers/%s/repos' % (self.BASE_URL, user['login'])
        try:
            response = self.session.request('GET', url, headers={
                'Accept': 'application/vnd.github.mercy-preview+json'
            })
            repos = response.json()
        except:
            repos = None
        self.cache['public_repos'] = repos
        return repos

    def get_integration(self):
        try:
            data = self.get('user/installations', headers={
                'Accept': 'application/vnd.github.machine-man-preview+json'
            })
        except:
            return None
        if data['total_count'] < 1:
            return None
        installations = data.get('integration_installations')
        if installations is None:
            return None
        app_id = app.config['GITHUB_APP_ID']
        for installation in installations:
            if installation['app_id'] == app_id:
                return installation
        return None

github = GitHub(app)
