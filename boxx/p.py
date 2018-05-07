#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
`import boxx.p` act same as `p()`

Notice: For Python 2 only first time import works 

useage:
    >>> import boxx.p
    
help(p) for more help
'''
from .ylsys import  py2
from .tool import p

deep = 6
if py2:
    deep = 1  

p(deep)

if not py2:
    from .tool import removeImportSelf
    removeImportSelf('boxx.p')

#from . import *
#print(prettyFrameStack())
#fs = getFatherFrames(endByMain=1)
#list(map(pipe(prettyFrameLocation,log),fs))


if __name__ == '__main__':
    pass

