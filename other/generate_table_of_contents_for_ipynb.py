#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 20:21:29 2018

@author: yanglei
"""

from boxx import *

import json

ipynb = json.loads(openread('../tutorial_for_boxx.ipynb'))

firstLines = [d['source'][0] for d in ipynb['cells'] if d['cell_type'] == 'markdown' and len(d['source'])]

heads = filter2(lambda x:x.strip().startswith('##'), firstLines)

'''
- [👀 Examples](#-examples)
  - [Section: Strain your brain!](#section-strain-your-brain)
    '''

md = '''


<!-- START `./other/generate_table_of_contents_for_ipynb.py` generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN `./other/generate_table_of_contents_for_ipynb.py` TO UPDATE -->


<h2>Table of Contents</h2>
'''
for h in heads:
    if h[-1] == '\n':
        h = h[:-1]
    if '### ' in h:
        bais = 4
    elif '## ' in h:
        bais = 3
    s = h[h.index('#') + bais:]
    href = s.replace('`', '').replace(' ', '-')
    mds = '[%s](#%s)\n'%(s, href)
#    if ')' in href:
#        mds = s+'\n'
    md += (bais-2)*'  ' + '- ' + mds
    
#printt-md
    
import markdown2
html = markdown2.markdown(md) 
html = html.replace('&lt;','<').replace('&gt;','>')
print(html)










