import flask_github

class GitHubHelper(flask_github.GitHub):
    def get_user(self):
        try:
            user = self.get('user')
        except:
            user = None
        return user

    def get_public_repos(self, username):
        if not username:
            return None
        url = '%susers/%s/repos' % (self.BASE_URL, username)
        try:
            response = self.session.request('GET', url, headers={
                'Accept': 'application/vnd.github.mercy-preview+json'
            })
            repos = response.json()
        except:
            return None
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
        app_id = self.app.config['GITHUB_APP_ID']
        for installation in installations:
            if installation['app_id'] == app_id:
                return installation
        return None
