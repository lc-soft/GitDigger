import flask_github

class GitHubHelper(flask_github.GitHub):
    def get_user(self):
        try:
            user = self.get('user')
        except:
            user = None
        return user

    def get_public_repo(self, full_name):
        if not full_name:
            return None
        url = '%srepos/%s' % (self.BASE_URL, full_name)
        try:
            response = self.session.request('GET', url, headers={
                'Accept': 'application/vnd.github.mercy-preview+json'
            })
            repo = response.json()
        except:
            return None
        return repo

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
