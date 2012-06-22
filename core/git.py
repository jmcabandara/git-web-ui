import os

class Git:
    def __init__(self,base):
        self.base = base

    def repos(self):
        return [os.path.dirname(e[0]) for e in os.walk(self.base) if os.path.basename(e[0]) == '.git']

    def log(self, repo):
        cmd = ' '.join(['git','--git-dir','%s/.git' % repo, 'log','--pretty=format:%h#%an#%ar#%s'])
        result = os.popen(cmd).readlines()
        split_by_slash = [line.split('#') for line in result]        
        return split_by_slash

    def commit_info(self, repo, rev):
        cmd = ' '.join(['git','--git-dir','%s/.git' % repo, 'show', rev])
        result = ''.join(os.popen(cmd).readlines())
        return result.decode('utf-8')
         
    
