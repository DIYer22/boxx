# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from .ylsys import py2


printf = print


if py2:
    unicode = __builtins__['unicode']
else:
    unicode = str

def isstr(s):
    '''
    `isinstance(s, str)` for compatibility both python 2/3
    '''
    return isinstance(s, (str, unicode))


class Classobj:
    ''' 兼容 python 2 的 classobj'''
    pass
classobj = type(Classobj)
def istype(objOrType):
    ''' 
    `isinstance(objOrType, type)` for compatibility both python 2/3
    '''
    return isinstance(objOrType, (type, classobj))


if not py2 and 0:
    __listRange__ = range
    range = lambda *x:list(__listRange__(*x))
    __rawOpen__ = open
    open = lambda *l:__rawOpen__(l[0],'r',-1,'utf8') if len(l) == 1 else __rawOpen__(l[0],l[1],-1,'utf8')

