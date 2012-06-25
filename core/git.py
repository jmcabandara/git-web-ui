import os
import re
from itertools import tee, izip

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

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
        
        commit = Commit(result)
        commit.build()

        return commit
         

class Commit:
    def __init__(self, data):
        self.data = data
        self.diffs = []
        
    def build(self):
        diff_indexes = [i for i, val in enumerate(self.data) if val.startswith('diff --git')]

        commit_data = self.data[0:diff_indexes[0]]

        self.commit = re.match('^commit (.*)', commit_data[0]).group(1)

        m_author = re.match('^Author: (.+) <(.+)>', commit_data[1])
        self.author_name = m_author.group(1)
        self.author_email = m_author.group(2)

        self.date = re.match('^Date:   (.*)', commit_data[2]).group(1)

        self.message = '\n'.join(commit_data[4:-1]).strip()

        diffbuilder = DiffBuilder()
        diffbuilder.build(self.data, diff_indexes)
        
        self.diffs = diffbuilder.diffs
 

class DiffBuilder:
    def __init__(self):
        self.diffs = [] 

    def build(self, data, indexes):
        if len(indexes) == 1:
            diff = Diff(data[indexes[0]:]).build()
            self.diffs.append(diff)
        else:
            for a, b in pairwise(indexes):
                diff = Diff(data[a:b]).build()
                self.diffs.append(diff)     
            
            diff = Diff(data[indexes[-1]:]).build()
            self.diffs.append(diff)

class Diff:
    def __init__(self, data):
        self.data = data

    def build(self):
        self.name = re.match('diff --git a/(.*) b/(.*)', self.data[0]).group(1) 
 
        self.mode = [v.split()[0].upper() for v in self.data if v.startswith('new ') or v.startswith('deleted ')]
        if not self.mode:
            self.mode = 'MODIFIED'
        else:
            self.mode = self.mode[0]

        # Hack: When file is empy add an extra line
        if self.mode == 'NEW' and len(self.data) < 4:
            self.data.append('')
            

        # Cleaning
        clean = { 'NEW':4, 'MODIFIED':3, 'DELETED':2 } 

        for i in range(clean[self.mode]):
            del self.data[0]

        line_count = len(self.data[1:])
        char_count = map(lambda s: len(s), self.data[1:])
        if line_count > 1000 or any(map(lambda i: i > 500, char_count)):
            self.code = '[Suppressed]'
        else:
            self.code = ''.join(self.data[1:]).decode('utf-8')

        return self


