# -*- coding:utf8 -*-
import os
import sys
import json
import codecs
import requests
from comment_fetcher import CommentFetcher

excludes = set([
    '.git',
    'build',
    'dist',
    'node_modules'
])

language_extensions = {
    'py': 'python',
    'cpp': 'cpp',
    'hpp': 'cpp',
    'h': 'cpp',
    'c': 'c',
    'js': 'javascript'
}

language_topics = {
    'python': 'Python',
    'c': 'C',
    'cpp': 'C++',
    'javascript': 'JavaScript'
}

class CommentDigger(object):
    FIXME_TAG = 'fixme:'
    LOG_CMD = 'git log --pretty=format:"%H" --max-count=1 -- {}'

    def __init__(self, debug=False):
        self.store = []
        self.debug = False

    def load(self, path, content, language):
        lines = content.split('\n')
        fetcher = CommentFetcher(language)
        for comment in fetcher.fetch(content):
            description = comment.content.strip()
            if description.lower().find(self.FIXME_TAG) != 0:
                continue
            snippet_start = comment.end + 1
            snippet_end = snippet_start + 16
            for line in lines[snippet_start:snippet_end]:
                if len(line.strip()) > 0:
                    break
                snippet_start += 1
            snippet_end = snippet_start + 16
            commit_id = os.popen(self.LOG_CMD.format(path)).read().strip()
            data = {
                'file': path,
                'line': comment.start,
                'commit_id': commit_id,
                'content': '\n'.join(lines[snippet_start:snippet_end]),
                'content_start_line': snippet_start,
                'content_end_line': snippet_end,
                'description': description[len(self.FIXME_TAG):].strip(),
                'language': language_topics[language]
            }
            self.store.append(data)

def digg(repo_dir='./', debug=False):
    cwd = os.getcwd()
    os.chdir(repo_dir)
    digger = CommentDigger(debug)
    for root, dirs, files in os.walk('./'):
        [dirs.remove(d) for d in list(dirs) if d in excludes]
        for f in files:
            path = os.path.join(root, f)
            extension = os.path.splitext(f)[1]
            language = language_extensions.get(extension[1:])
            if language is None:
                continue
            content = open(path, 'rt').read()
            if content[:3] == codecs.BOM_UTF8:
                content = content[3:]
            if os.sep != '/':
                path = path.replace(os.sep, '/')
            path = path[2:].decode()
            digger.load(path, content.decode('utf8'), language)
    f = open('snippets.json', 'wt+')
    f.write(json.dumps(digger.store, indent=2, sort_keys=True))
    f.close()
    os.chdir(cwd)

def upload(path, repo, username, password):
    f = open(path, 'rt')
    if f is None:
        return
    snippets = json.loads(f.read())
    url = 'http://gitdigger.io/api/repos/{}/snippets'.format(repo)
    r = requests.put(url, json=snippets, auth=(username, password))
    print 'response', r.status_code
    print json.dumps(r.json(), sort_keys=True, indent=2)

# FIXME: use command-line options parser to refactor it
if __name__ == '__main__':
    argv = sys.argv
    if len(argv) > 2:
        if argv[1] == 'digg':
            digg(sys.argv[2])
        elif argv[1] == 'upload':
            upload(argv[2], argv[3], argv[4], argv[5])
