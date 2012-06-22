import os
from subprocess import check_output
from flask import Flask, render_template, session, flash

DEBUG = True
SECRET_KEY = 'abcd123'

BASE_REPO_DIR = '/home/xterm/.venv/'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def repos():
    error = None
    repo_paths = [os.path.dirname(e[0]) for e in os.walk(BASE_REPO_DIR) if os.path.basename(e[0]) == '.git']
    if not repo_paths:
        error = 'No repositories found!'

    logs = {}

    for repo in repo_paths: 
        result = check_output(['git','--git-dir','%s/.git' % repo, 'log','--pretty=format: %h|%an|%ar|%s'])
        split_by_line = result.split('\n')
        split_by_slash = [line.split('|') for line in split_by_line]        
        logs[repo.split('/')[-1]] = split_by_slash

    return render_template('index.html', logs=logs, error=error, basedir=BASE_REPO_DIR)

if __name__ == '__main__':
    app.run()
