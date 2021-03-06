import os
import sys
from flask import Flask, render_template, flash
from core.git import Git

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# App specific settings

BASE_REPO_DIR = os.path.expanduser('~') 
if len(sys.argv) > 1:
    BASE_REPO_DIR = sys.argv[1]

# Collect info
git = Git(BASE_REPO_DIR)
repo_paths = git.repos()

# Views
@app.route('/')
def repos():
    error = None
    if not repo_paths:
        error = 'No repositories found!'

    repos = {}

    for repo in repo_paths:
        repos[os.path.split(repo)[-1]] = repo

    return render_template('index.html', repos=repos, error=error, basedir=BASE_REPO_DIR)


@app.route('/<repo_name>')
def commits(repo_name):
    error = None

    logs =  [(repo_name,git.log(x)) for x in repo_paths if x.endswith(repo_name)][0]

    return render_template('repo.html', logs=logs, error=error, basedir=BASE_REPO_DIR)

@app.route('/<repo_name>/<rev>')
def commit_info(repo_name,rev):
    repo_path = filter(lambda repo: repo.endswith(repo_name), repo_paths)[0]
    commit = git.commit_info(repo_path, rev)    

    return render_template('diff.html', commit=commit, repo=repo_name, rev=rev) 

if __name__ == '__main__':
    app.run()
