#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
`import boxx.g` act same as `g()`

useage:
    >>> import boxx.g
        
Instruct
----------
    your can exec `g()`, `p()` in any function or module
    all vars that belong the function will transport to
    Python interactive shell. and `globals()` will in `p` which is a dicto
    the differtent between `g` and `gg` is that `gg` will auto print the vars's information
    
    BTW, `import boxx.g`, `import boxx.p` is convenient way to use `g()` without `from boxx import g`
    
Notice
-----------
    For Python 2 only first time import works 

    在函数内运行`p()` or `lc()`  
    则此函数的global和local 变量会载入全局变量 p 中
    函数的 frame等其他信息 则放入全局变量 lc

'''
from .ylsys import  py2
from .tool import out

deep = 6
if py2:
    deep = 1  

out(deep, printt=False)

if not py2:
    from .tool import removeImportSelf
    removeImportSelf('boxx.g')


if __name__ == '__main__':
    pass
