#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 00:55:51 2018

@author: leiYang
"""
from __future__ import unicode_literals, print_function


from boxx import *
test = True
#test = False
if test:
    from toolTest import *
    
    from ylimgTest import *
    
    from ylmlTest import *



l = []
def f(t, tt=0):
    print(t, tt)
    with timeit(0):
        time.sleep((t+1)*.01+.1)
        a=prettyFrameLocation()
        b=prettyFrameStack()
    r = str(t)
    l.append(r)
    return r
ts = ll-range(20000)
kv={
    'thread':1,
    'pool':2,
#    chunksize=1,
    'logfreq':2,
    }



iterables = [ts,ts]
fun = f
if __name__ == '__main__':

    pass
tree






