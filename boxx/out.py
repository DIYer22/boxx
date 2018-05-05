#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
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

#from .tool import BoxxException, prettyFrameLocation
#import sys
#sys.modules.pop('boxx.out')
#class BoxxOutStop(BoxxException):
#    pass
#stop = '\x1b[36m%s\x1b[0m'%'rasied at '
#callPath = prettyFrameLocation(sys._getframe(deep))
#raise BoxxOutStop(stop + callPath)
#from . import *
#print(prettyFrameStack())
#fs = getFatherFrames(endByMain=1)
#list(map(pipe(prettyFrameLocation,log),fs))
if __name__ == '__main__':
    pass
