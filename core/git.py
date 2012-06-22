import os
from subprocess import check_output

class Git:
    def __init__(self,base):
        self.base = base

    def repos(self):
        return [os.path.dirname(e[0]) for e in os.walk(self.base) if os.path.basename(e[0]) == '.git']

    def log(self, repo):
        result = check_output(['git','--git-dir','%s/.git' % repo, 'log','--pretty=format:%h|%an|%ar|%s'])
        split_by_line = result.split('\n')
        split_by_slash = [line.split('|') for line in split_by_line]        
        return split_by_slash

    def commit_info(self, repo, rev):
        result = check_output(['git','--git-dir','%s/.git' % repo, 'show', rev])
        return result 
         
    
