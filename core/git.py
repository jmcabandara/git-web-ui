import os
import re

class Git:
    def __init__(self,base):
        self.base = base

    def repos(self):
        return [os.path.dirname(e[0]).decode('utf-8') for e in os.walk(self.base) if os.path.basename(e[0]) == '.git']

    def log(self, repo):
        cmd = ' '.join(['git','--git-dir', os.path.join(repo,'.git'), 'log','--pretty=format:%h#%an#%ar#%s'])
        result = os.popen(cmd).readlines()
        split_by_slash = [line.split('#') for line in result]        
        return split_by_slash

    def commit_info(self, repo, rev):
        cmd = ' '.join(['git','--git-dir', os.path.join(repo,'.git'), 'show', rev])
        result = os.popen(cmd).readlines()
        file_dict = {}
        current_file = None
        skipping = False
        for line in result:
            m = re.match(r'\+\+\+ b/(.+)',line)
            m1 = re.match(r'diff --git .*',line)
            if m:
                current_file = m.group(1)
                file_dict[current_file] = []
                skipping = False
            elif m1:
                skipping = True 
            elif current_file and not skipping:
                file_dict[current_file].append(line)

        return dict([(k,''.join(v)) for (k,v) in file_dict.items()])  
         
    
