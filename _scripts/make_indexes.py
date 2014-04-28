#!/usr/bin/env python 

import os
import json

root_dir = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

notebook_dirs = {}

t="""---
layout: default
title: {title}
---

{links}

"""


for root, dirs, files in os.walk(root_dir):
    nb_files = [f for f in files if f.endswith('.ipynb')]
    if len(nb_files):
        notebook_dirs[root] = nb_files
        
for dir_, files in notebook_dirs.items():
    links = []
    path = dir_.split('/').pop()
    for fn in files:
        
        if fn.startswith('_'):
            continue
        
        title = fn.replace('.ipynb','')
        plain_file = title.replace(' ','_')+'.html'
        code_file = title.replace(' ','_')+'-code.html'
        
        link = "* [{}]({})".format(title, plain_file)
        
        links.append(link)
        
        
    content = t.format(title=path.title(), links='\n'.join(links))
        
    with open(os.path.join(dir_, 'index.md'),'w') as f:
        f.write(content)
        
        
            
        
    