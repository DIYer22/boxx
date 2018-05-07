# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from .ylsys import py2
import os, sys, warnings
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
    reduce
    glob = globals()
    for name in funForAutoList:
        rawf = glob[name] if name in glob else  __builtins__[name]
        glob[name+'2'] = addListAfter(rawf)

setFuncation2ForAutoList()


def setDisplayEnv():
    msg = '''%s
        os.environ["DISPLAY"] not found, may cuse error like this 
        [QXcbConnection Error](https://github.com/ipython/ipython/issues/10627)
        so, we auto set os.environ["DISPLAY"] = ":0"    '''%'\x1b[36m%s\x1b[0m'% 'warning from boxx'
    f = sys._getframe(0)
    c = f.f_code
    warnings.warn_explicit(msg, RuntimeWarning, c.co_filename, c.co_firstlineno, module='boxx')
    os.environ["DISPLAY"] = ":0"
if 'DISPLAY' not in os.environ:
    setDisplayEnv()

if not py2 and 0:
    __rawOpen__ = open
    open = lambda *l:__rawOpen__(l[0],'r',-1,'utf8') if len(l) == 1 else __rawOpen__(l[0],l[1],-1,'utf8')

