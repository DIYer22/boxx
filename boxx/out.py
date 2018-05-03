#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
useage:
    >>> import boxx.out
    
help(out) for more help
'''
from . import out, py2
if py2:
    out(1)
else:
    out(6)
#from . import *
#print(prettyFrameStack())
#fs = getFatherFrames(endByMain=1)
#list(map(pipe(prettyFrameLocation,log),fs))
if __name__ == '__main__':
    pass
