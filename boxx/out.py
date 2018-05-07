#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
`import boxx.out` act same as `out()`

Notice: For Python 2 only first time import works 

useage:
    >>> import boxx.out
    
help(out) for more help
'''
from .ylsys import  py2
from .tool import out

deep = 6
if py2:
    deep = 1  

out(deep)

if not py2:
    from .tool import removeImportSelf
    removeImportSelf('boxx.out')


#callPath = prettyFrameLocation(sys._getframe(deep))
#raise BoxxOutStop(stop + callPath)
#from . import *
#print(prettyFrameStack())
#fs = getFatherFrames(endByMain=1)
#list(map(pipe(prettyFrameLocation,log),fs))
if __name__ == '__main__':
    pass
