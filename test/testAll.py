#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 00:55:51 2018

@author: leiYang
"""
from __future__ import unicode_literals, print_function

#what-
from boxx import *
import boxx
test = True
test = False
if test:
    from toolTest import *
    
    from ylimgTest import *
    
    from ylmlTest import *

pattern = 'TODO'
findinRoot(pattern,root='..')
#findinRoot(up=pattern,root='..')
#replaceAllInRoot(pattern,'Function',root='..')


if __name__ == '__main__0':
    pass
    from boxx.ylth import *
    
    def f(self,*l, **kv):
        init = self.__init__
        code = init.__code__
        ca = code.co_argcount
        cv = code.co_varnames
#        type(self)()
        
#        log-prettyFrameStack()
        frames = getFatherFrames(1)
        for f in frames:
            log-f.f_code.co_name
            if f.f_code.co_name != '__init__':
                break
            loc = f.f_locals
#        tree-loc
        args = {k:loc[k] for k in cv}
        tree-args
        rawModuleInit(self)
#        out()
#        g.f = frames = getFatherFrames()
#        p/map2(lambda f:f.f_locals.get('self'),frames[::])
#        tree-locals()
    nn.Module.__init__
    
#    class nnModule(nn.Module):
#        def __init__(self, *l, **kv):
#            log-prettyFrameStack()
    if '__init__' in str(nn.Module.__init__):
        rawModuleInit = nn.Module.__init__
    nn.Module.__init__ = f
#        nn.Module = nnModule
#    conv = nn.Conv2d(1,2,(3,3))
    class Mo(nn.Module):
        def __init__(self,b='b',**l):
            super(Mo, self).__init__()
    a= Mo('a')
    
#    what- a.__init__.__code__


    fs=g.f


