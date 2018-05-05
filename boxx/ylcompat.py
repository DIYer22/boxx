# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from .ylsys import py2
from functools import reduce, wraps

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


def setFuncation2ForAutoList():
    '''
    add funcation 'range2', 'map2', 'reduce2', 'zip2' that retrun a list like python2
    '''
    funForAutoList = ['range', 'map', 'reduce', 'filter', 'zip']
    if py2:
        addListAfter = lambda x:x
    else:    
        def addListAfter(f):
            @wraps(f)
            def innerF(*l, **kv):
                r = f(*l, **kv)
                return list(r)
            return innerF
    
    glob = globals()
    for name in funForAutoList:
        rawf = glob[name] if name in glob else  __builtins__[name]
        glob[name+'2'] = addListAfter(rawf)

setFuncation2ForAutoList()


if not py2 and 0:
    __rawOpen__ = open
    open = lambda *l:__rawOpen__(l[0],'r',-1,'utf8') if len(l) == 1 else __rawOpen__(l[0],l[1],-1,'utf8')

