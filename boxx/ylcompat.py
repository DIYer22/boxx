# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import sys
from .ylsys import py2

if py2:
    unicode = __builtins__['unicode']
else:
    unicode = str


printf = print

if not py2 and 0:
    __listRange__ = range
    range = lambda *x:list(__listRange__(*x))
    __rawOpen__ = open
    open = lambda *l:__rawOpen__(l[0],'r',-1,'utf8') if len(l) == 1 else __rawOpen__(l[0],l[1],-1,'utf8')

