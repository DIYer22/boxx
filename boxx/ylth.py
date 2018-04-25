#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
sysc.py: system config
'''
from __future__ import unicode_literals

from . import *
from .ylsys import cpun, cloud, cuda, usecuda
import torch
from torch.autograd import Variable
import torch.utils.data
th = torch
nn = th.nn


# default whether choose cuda
#th.long = torch.cuda.LongTensor 
#th.double = torch.cuda.DoubleTensor 
#th.int = torch.cuda.IntTensor 
#th.short = torch.cuda.ShortTensor 
#th.byte = torch.cuda.ByteTensor 
#th.half = torch.cuda.HalfTensor 
#th.char = torch.cuda.CharTensor 
#th.float = torch.cuda.FloatTensor 

if (not cuda and usecuda=='auto') or not usecuda:
    cudaAttri =  lambda self,*l,**kv:self
    nn.Module.cuda = cudaAttri
    Variable.cuda = cudaAttri
    
    torch.nn.DataParallel = cudaAttri
    
    class withh():
        def __init__(self, *l):
            pass
        def __call__(self):
            return self
        def __enter__(self):
            return self
        def __exit__(self, typee, value, traceback):
            pass
    torch.cuda.device = withh

    th.cuda.LongTensor = th.LongTensor
    th.cuda.DoubleTensor = th.DoubleTensor
    th.cuda.IntTensor = th.IntTensor
    th.cuda.ShortTensor = th.ShortTensor
    th.cuda.ByteTensor = th.ByteTensor
    th.cuda.HalfTensor = th.HalfTensor
    th.cuda.CharTensor = th.CharTensor
    th.cuda.FloatTensor = th.FloatTensor
    
    rawDataLoader = th.utils.data.DataLoader
    from functools import wraps    
    def warp(f):
        @wraps(f)
        def DataLoader(*l, **kv):
            if 'pin_memory' in kv:
                kv.pop('pin_memory')
            r = f(*l, **kv)
            return r
        return DataLoader
    th.utils.data.DataLoader = warp(th.utils.data.DataLoader)
if __name__ == '__main__':
    l = ['LongTensor',
     'DoubleTensor',
     'IntTensor',
     'ShortTensor',
     'ByteTensor',
     'HalfTensor',
     'CharTensor',
     'FloatTensor']
    formatt = 'th.cuda.%s = th.%s'
    print('\n'.join([formatt%(i,i) for i in l]))

        
    
