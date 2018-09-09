#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
sysc.py: system config
'''
from __future__ import unicode_literals
from . import *
from .ylsys import cpun, cloud, cuda, usecuda
from .ylimg import npa, r
from .tool import FunAddMagicMethod, nextiter, withfun, pred

from .ylcompat import py2, ModuleNotFoundError

def importYlthRequire(exc_type, exc_value, exc_traceback):
    if exc_type is ModuleNotFoundError:
        pred('''\n\nMesage from boxx:\n\tTo use boxx.ylth, you should run: \n\t`pip install torchvision torchsummary torchviz`\n''')
with withfun(exitFun=importYlthRequire, exception=True):
    from torchsummary import summary
#    import torchviz

#import matplotlib.pyplot as plt
#import skimage.io as sio
#import skimage.data as sda
from collections import OrderedDict
from functools import wraps

#if 'torch' in sys.modules:
#    del sys.modules[('torch')]
#    sys.modules.pop('torch')
#from imp import reload  
#reload(torch)
#reload(torch.nn)
#reload(torch.nn.modules.module)
#import importlib
#torch = importlib.reload(torch)
from torch.autograd import Variable
import torch.utils.data
th = torch
nn = th.nn
from torch.nn import (Conv2d, Linear, ConvTranspose2d, BatchNorm2d, ReLU, Tanh, 
                      Softmax2d, CrossEntropyLoss, DataParallel, MSELoss, 
                      MaxPool2d, AvgPool2d, Module, functional, Sequential)
Tensor = torch.Tensor
F = functional

import torchvision.transforms as transforms
import torchvision.datasets as datasets

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
nn.Module.summary = lambda self, inputShape=None, group=None, gen=None:summary(self, inputShape or getDefaultInputShape(self, group, gen))


def dedp(model):
    '''get raw model instead of torch.nn.DataParallel '''
    return model.module if isinstance(model, torch.nn.DataParallel) else model

if 'Module' in str(torch.nn.Module.load_state_dict):
    torch.rawModule = rawModule = torch.nn.Module.load_state_dict
else :
    rawModule = torch.rawModule 
def tryLoad(self, state_dict, strict=True):
    try:
        rawModule(self, state_dict, strict)
    except (KeyError,RuntimeError) as e:
        print('\x1b[31m%s\x1b[0m' % '\n"try strict=False! in Module.load_state_dict() " messge from boxx.ylth \n')
        para = state_dict
        para = OrderedDict(
                    [(k.replace('module.', ''),v) for k,v in para.items()]
            )
        rawModule(self, para, strict)
def toCpu():            
    cudaAttri =  lambda self,*l,**kv:self
    nn.Module.cuda = cudaAttri
    Variable.cuda = cudaAttri
    torch.Tensor.cuda = cudaAttri
    torch.Tensor.to = cudaAttri
    
#    class FakeDataParallel(torch.nn.DataParallel):
#        def __init__(self, x):
#            super(FakeDataParallel, self).__init__()
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
    from boxx import fnone
    torch.cuda.set_device = fnone
    torch.cuda.is_available = lambda :True
    

    th.cuda.LongTensor = th.LongTensor
    th.cuda.DoubleTensor = th.DoubleTensor
    th.cuda.IntTensor = th.IntTensor
    th.cuda.ShortTensor = th.ShortTensor
    th.cuda.ByteTensor = th.ByteTensor
    th.cuda.HalfTensor = th.HalfTensor
    th.cuda.CharTensor = th.CharTensor
    th.cuda.FloatTensor = th.FloatTensor
    
    rawDataLoader = th.utils.data.DataLoader
#    def warp(f):
#        @wraps(f)
#        def DataLoader(*l, **kv):
#            if 'pin_memory' in kv:
#                kv.pop('pin_memory')
#            r = f(*l, **kv)
#            return r
#        return DataLoader
    
    class DataLoaderForCPU(rawDataLoader):
        def __init__(self, *l, **kv):
            rawDataLoader.__init__(self, *l, **kv)
            self.pin_memory = False
        
    th.utils.data.DataLoader = DataLoaderForCPU
    
    rawThLoad = torch.load
    def torchLoad(*l, **kv):
        return rawThLoad(*l,**(kv.update({'map_location':'cpu'}) or kv))
    torch.load = torchLoad

            
    nn.Module.load_state_dict = tryLoad
    torch.nn.modules.module.Module.load_state_dict = tryLoad

usecpu = (not cuda and usecuda=='auto') or not usecuda
if usecpu:
    toCpu()
_TensorBase = torch._TensorBase if '_TensorBase' in dir(torch) else torch._C._TensorBase

def tht(t):
    '''
    anything t to torch.Tensor
    '''
    if not isinstance(t, _TensorBase):
        t = th.from_numpy(npa-t).cuda()
    return t.cuda()
tht = FunAddMagicMethod(tht)

t = tht(r).float()

@wraps(torch.autograd.Variable)
def var(t, *l,  **kv):
    t = tht(t)
    t = Variable(t, *l, **kv)
    return t.cuda()
var = FunAddMagicMethod(var)


def kaimingInit(model):
    stateDict = model.state_dict()
    for key in stateDict:
        tag = 0
        t = stateDict[key]
        
        if (t.ndimension()==4 and t.shape[-1]>2) or 'conv' in key:
            nn.init.kaiming_normal(stateDict[key], mode='fan_out')
            tag = 1
        elif 'bn' in key and 'weight' in key:
            stateDict[key][...] = 1
            tag = 1
        elif 'bias' in key :
            stateDict[key][...] = 0
            tag = 1
        elif 'fc' in key and t.ndimension()==2:
            nn.init.kaiming_normal(t)


def getDefaultInputShape(model, group=None, gen=None):
    para = nextiter(model.parameters())
    shape = para.shape
    if len(shape) == 4 and shape[-1]>2 :
        default = (shape[1], 244, 244)
    elif len(shape) == 4 and shape[-1] == shape[-2] == 1  :
        default = (shape[1], 244, 244)
        if gen:
            default = (shape[1], 1, 1)
    elif len(shape) == 2:
        default = (shape[1],)
    if group:
        default = (shape[1]*group, 244, 244)
    return default
    
class HookRegister():
    def __init__(self, module, hook, direct='f'):
        self.hook = hook
        self.hooks = hooks = []
        self.module = module
        
        def apply(module):
            if direct == 'f':
                hooks.append(module.register_forward_hook(hook))
            elif direct == 'b':
                hooks.append(module.register_backward_hook(hook))
        module.apply(apply)
    def remove(self):
        for h in self.hooks:
            h.remove()
    def __enter__(self):
        return self
    def __exit__(self,*l):
        self.remove()
def removeAllHook(module):
    def apply(module):
        module._forward_hooks=OrderedDict()
    module.apply(apply)

from boxx import log, ylimgTool, out
ar= FunAddMagicMethod(lambda x: log-ylimgTool.prettyArray(x))

def hasnan(t):
    nan = th.isnan(t).sum()
    if nan :
        out(1)
        ar(t)
        raise LookupError('Has torch.nan')
    
def getpara(m):
    '''get first parameter'''
    return nextiter(m.parameters())

def getpara0(m):
    return getpara(m).view(-1)[0]
def getgrad(m):
    return getpara(m).grad
def getgrad0(m):
    grad = getpara(m).grad
    return None if grad is None else grad.view(-1)[0]
getpara, getpara0, getgrad, getgrad0 = map(FunAddMagicMethod, [getpara, getpara0, getgrad, getgrad0])

def vizmodel(m, shape=None):
    if shape is None:
        shape = (1,) + getDefaultInputShape(m)
    from torchviz import make_dot
    x = th.rand(shape)
    x.to(getpara(m))
    graph = make_dot(m(x), params=dict(m.named_parameters()))
    return graph

def flatten(t, dim=-1):
    '''
    >>> t = shape(1,2,3,4) 
    >>> flatten(t, dim=-2)
    shape(1,6,4)
    '''
    shape = list(t.shape)
    shape[dim-1] *= shape[dim]
    shape.pop(dim)
    return t.reshape(tuple(shape))


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

        
    
