#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 00:55:51 2018

@author: leiYang
"""
from __future__ import unicode_literals, print_function

#what-
from boxx import *
test = True
test = False
if test:
    from toolTest import *
    
    from ylimgTest import *
    
    from ylmlTest import *

from collections import defaultdict

class withfun():
    def __init__(self, enterFun=None, exitFun=None):
        self.enterFun = enterFun
        self.exitFun = exitFun
    def __enter__(self):
        if self.enterFun:
            self.enterFun()
    def __exit__(self,*l):
        if self.exitFun:
            self.exitFun()

class withattr(withfun):
    def __init__(self, obj, attrs):
        self.obj = obj
        self.attrs = attrs
        d = obj 
        
        sett = (lambda d, k, v: d.__setitem__(k, v)) if isinstance(obj, dict) else setattr
        get = (lambda d, k: d[k]) if isinstance(obj, dict) else getattr
        pop = (lambda d, k: d.pop(k)) if isinstance(obj, dict) else delattr
        has = (lambda d, k: k in d) if isinstance(obj, dict) else hasattr
        def enterFun():
            self.old = {}
            for k,v in attrs.items():
                if has(d, k) :
                    self.old[k] = get(d, k)
                sett(d, k, v)
                
        def exitFun():
            for k in attrs.keys():
                pop(d, k)
            if isinstance(d, dict):
                d.update(self.old)
            else:
                for k, v in self.old.items():
                    sett(d, k, v)
        super(withattr, self).__init__(enterFun, exitFun)
    

d = dict(enumerate(ll))
d = timeit

da = dira
if isinstance(d, dict):
    da =  tree

da-d

with withattr(d, {'aa':1}):
    da-d
#    d.aa
da-d

tree- d.__dict__

wf = withfun(9)

pattern = '[id(self)]'
#findinRoot(up=pattern,root='..')
#replaceAllInRoot(pattern,'printfreq',root='..')


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


