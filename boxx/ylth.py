#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
sysc.py: system config
'''
from __future__ import unicode_literals

from . import *
from .ylsys import cpun, cloud, cuda, usecuda
from .ylimg import npa
from collections import OrderedDict
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

# add summary to torch.nn.Module
from torchsummary import summary
nn.Module.summary = lambda self, inputShape=(3,244,244):summary(self, inputShape)


usecpu = (not cuda and usecuda=='auto') or not usecuda
if usecpu:
    cudaAttri =  lambda self,*l,**kv:self
    nn.Module.cuda = cudaAttri
    Variable.cuda = cudaAttri
    torch.Tensor.cuda = cudaAttri
    
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
    
    rawThLoad = torch.load
    def torchLoad(*l, **kv):
        return rawThLoad(*l,**(kv.update({'map_location':'cpu'}) or kv))
    torch.load = torchLoad
    
    rawModule = torch.nn.Module.load_state_dict
    def tryLoad(self, state_dict, strict=True):
        try:
            rawModule(self, state_dict, strict)
        except KeyError as e:
            print('\x1b[31m%s\x1b[0m' % '\n"try strict=False! in Module.load_state_dict() " messge from boxx.ylth \n')
            para = state_dict
            para = OrderedDict(
                        [(k.replace('module.', ''),v) for k,v in para.items()]
                )
            rawModule(self, para, strict)
            
    nn.Module.load_state_dict = tryLoad
    
def tht(t):
    return th.from_numpy(npa-t).cuda()
    
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

        
    
