#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statistics tools 

@author: yl
"""
import numpy as np
from functools import wraps

def Distribution(f):
    '''
    return  distribution of bias round v and max bias is @maxratio*v.mean() or @maxbias
    '''
    @wraps(f)
    def innerF(v,maxbias=None,  maxratio=.2, *l, **kv):
        mean = v
        if maxbias is None:
            if isinstance(v, np.ndarray):
                mean = v.mean()
            maxbias = maxratio*mean
        biass = f(v=v, maxbias=maxbias, maxratio=maxratio, *l, **kv)
        return v + biass
    return innerF
        

@Distribution
def distnorm(v, maxbias=None, maxratio=.2, std=2, ):
    '''
    return normal distribution of bias round v and max bias is @maxratio*v.mean() or @maxbias
    '''
    shape=None
    if isinstance(v, np.ndarray):
        shape = v.shape
    normaBiass = np.random.normal(loc=1, scale=1./std, size=shape)%(2) - 1
    
    biass = normaBiass * maxbias
    return biass

@Distribution
def distavg(v, maxbias=None, maxratio=.2, ):
    '''
    return uniform distribution of bias round v and max bias is @maxratio*v.mean() or @maxbias
    '''
    shape=None
    if isinstance(v, np.ndarray):
        shape = v.shape
    biass = np.random.uniform(-maxbias, maxbias, size=shape)
    return biass



if __name__ == "__main__":
    from boxx import loga
    loga-distavg(np.ones((517,111)))
    loga-distnorm(np.ones((517,111)),3, std=4)
    pass
    
    
