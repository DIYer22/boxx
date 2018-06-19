#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
`import boxx.p` act same as `p()`

Notice: For Python 2 only first time import works 

useage:
    >>> import boxx.p
    
        
Instruct
----------
    your can use `out()`, `p()` in any function or module
    exec `out()`, all vars that belong the function will transport to
    Python interactive shell. and `globals()` will in `p` which is a dicto
    
    BTW, `import boxx.out`, `import boxx.p` is convenient way to use `out()` without `from boxx import out`
    
    在函数内运行`p()` or `lc()`  
    函数的 frame等其他信息 则放入全局变量 lc

'''
from .ylsys import  py2
from .tool import p

deep = 6
if py2:
    deep = 1

p(deep)

if py2:
    import sys
    sys.modules['boxx.p'] = p
else:
    from .tool import removeImportSelf
    removeImportSelf('boxx.p')
#from . import *
#print(prettyFrameStack())
#fs = getFatherFrames(endByMain=1)
#list(map(pipe(prettyFrameLocation,log),fs))


if __name__ == '__main__':
    pass

