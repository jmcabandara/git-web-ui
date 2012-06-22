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

# Views

@app.route('/')
def repos():
    error = None
    git = Git(BASE_REPO_DIR)    
    repo_paths = git.repos()
    if not repo_paths:
        error = 'No repositories found!'

    logs = {}

    for repo in repo_paths: 
        logs[repo] = git.log(repo) 

    return render_template('index.html', logs=logs, error=error, basedir=BASE_REPO_DIR)

if __name__ == '__main__':
    app.run()
