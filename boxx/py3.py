# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
#py3
pyv = sys.version_info.major
py3 = pyv == 3
if py3:
    __listRange__ = range
    range = lambda *x:list(__listRange__(*x))
    __rawOpen__ = open
    open = lambda *l:__rawOpen__(l[0],'r',-1,'utf8') if len(l) == 1 else __rawOpen__(l[0],l[1],-1,'utf8')

