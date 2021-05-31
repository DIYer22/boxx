#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
sysc.py: system config
"""
from __future__ import unicode_literals
import numpy as np
from .. import *
from ..ylsys import cpun, cloud, cuda, usecuda
from ..ylimg import npa, r
from ..tool import FunAddMagicMethod, nextiter, withfun, pred

from ..ylcompat import py2


from collections import OrderedDict
from functools import wraps
import matplotlib.pyplot as plt
import skimage.data as sda


from torch.autograd import Variable
import torch.utils.data

th = torch
nn = th.nn
from torch.nn import (
    Conv2d,
    Linear,
    ConvTranspose2d,
    BatchNorm2d,
    ReLU,
    Tanh,
    Softmax2d,
    CrossEntropyLoss,
    DataParallel,
    MSELoss,
    MaxPool2d,
    AvgPool2d,
    Module,
    functional,
    Sequential,
)

Tensor = torch.Tensor
F = functional

import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets


# add summary to torch.nn.Module
nn.Module.summary = lambda self, inputShape=None, group=None, ganNoise=False: __import__(
    "torchsummary"
).summary(
    self,
    inputShape or getModelDefaultInputShape(self, group, ganNoise),
    device=["cuda", "cpu"]["cpu" in str(getpara(self).device)],
)


def dedp(model):
    """get raw model instead of torch.nn.DataParallel """
    return model.module if isinstance(model, torch.nn.DataParallel) else model


if "Module" in str(torch.nn.Module.load_state_dict):
    torch.rawModule = rawModule = torch.nn.Module.load_state_dict
else:
    rawModule = torch.rawModule


def tryLoad(self, state_dict, strict=True):
    try:
        rawModule(self, state_dict, strict)
    except (KeyError, RuntimeError):
        print(
            "\x1b[31m%s\x1b[0m"
            % '\n"try strict=False! in Module.load_state_dict() " messge from boxx.ylth \n'
        )
        para = state_dict
        para = OrderedDict([(k.replace("module.", ""), v) for k, v in para.items()])
        rawModule(self, para, strict)


def toCpu():
    cudaAttri = lambda self, *l, **kv: self
    nn.Module.cuda = cudaAttri
    Variable.cuda = cudaAttri
    torch.Tensor.cuda = cudaAttri
    torch.Tensor.to = cudaAttri

    #    class FakeDataParallel(torch.nn.DataParallel):
    #        def __init__(self, x):
    #            super(FakeDataParallel, self).__init__()
    torch.nn.DataParallel = cudaAttri

    class withh:
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
    torch.cuda.is_available = lambda: True
    torch.cuda.device_count = lambda *l: 0

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
        return rawThLoad(*l, **(kv.update({"map_location": "cpu"}) or kv))

    torch.load = torchLoad

    nn.Module.load_state_dict = tryLoad
    torch.nn.modules.module.Module.load_state_dict = tryLoad


usecpu = (not cuda and usecuda == "auto") or not usecuda
if usecpu:
    toCpu()
_TensorBase = torch._TensorBase if "_TensorBase" in dir(torch) else torch._C._TensorBase


def tht(t):
    """
    anything t to torch.Tensor
    """
    if not isinstance(t, _TensorBase):
        t = th.from_numpy(npa - t).cuda()
    return t.cuda()


tht = FunAddMagicMethod(tht)

# t = tht(r).float()
t = th.from_numpy(r).float()
if cuda:
    t = t.cuda()


def recursive_func(func):
    def inner_func(batch, device=None):
        if isinstance(batch, dict):
            return {k: inner_func(v) for k, v in batch.items()}
        elif isinstance(batch, (list, tuple)):
            return type(batch)([inner_func(x) for x in batch])
        else:
            return func(batch, device=device)

    return inner_func


def to_tensor(x, device=None):
    if isinstance(x, np.ndarray):
        x = torch.from_numpy(x)
    if isinstance(x, torch.Tensor):
        x = x.cuda() if device is None else x.to(device)
    return x


batch_to_tensor = recursive_func(to_tensor)


def to_numpy(x, device=None):
    if isinstance(x, torch.Tensor):
        x = x.cpu().numpy()
    return x


batch_to_numpy = recursive_func(to_numpy)


def batchToTensor(batch, device=None):
    """
    turn a dataloader's batch to tensor (from dpflow).
    support dict, list, tuple as a batch
    """

    def to_tensor(x):
        if isinstance(x, np.ndarray):
            x = torch.from_numpy(x)
        if isinstance(x, torch.Tensor):
            x = x.cuda() if device is None else x.to(device)
        return x

    if isinstance(batch, dict):
        return {k: to_tensor(v) for k, v in batch.items()}
    if isinstance(batch, (list, tuple)):
        return [to_tensor(v) for v in batch]


def batchToNumpy(batch):
    """
    turn a dataloader's batch to numpy (for dpflow).
    support dict, list, tuple as a batch
    """
    if isinstance(batch, dict):
        return {
            k: (v.cpu()).numpy() if isinstance(v, torch.Tensor) else v
            for k, v in batch.items()
        }
    if isinstance(batch, (list, tuple)):
        return [(v.cpu()).numpy() if isinstance(v, torch.Tensor) else v for v in batch]


@wraps(torch.autograd.Variable)
def var(t, *l, **kv):
    t = tht(t)
    t = Variable(t, *l, **kv)
    return t.cuda()


var = FunAddMagicMethod(var)


def kaimingInit(model):
    stateDict = model.state_dict()
    for key in stateDict:
        tag = 0
        t = stateDict[key]

        if (t.ndimension() == 4 and t.shape[-1] > 2) or "conv" in key:
            nn.init.kaiming_normal(stateDict[key], mode="fan_out")
            tag = 1
        elif "bn" in key and "weight" in key:
            stateDict[key][...] = 1
            tag = 1
        elif "bias" in key:
            stateDict[key][...] = 0
            tag = 1
        elif "fc" in key and t.ndimension() == 2:
            nn.init.kaiming_normal(t)


def getModelDefaultInputShape(model, group=None, ganNoise=False):
    para = nextiter(model.parameters())
    shape = para.shape
    if len(shape) == 4 and shape[-1] > 2:
        default = (shape[1], 244, 244)
    elif len(shape) == 4 and shape[-1] == shape[-2] == 1:
        default = (shape[1], 244, 244)
        if ganNoise:
            default = (shape[1], 1, 1)
    elif len(shape) == 2:
        default = (shape[1],)
    if group:
        default = (shape[1] * group, 244, 244)
    return default


def genModelInput(model, inputShape=None, group=None, ganNoise=False, batchn=2):
    """
    Auto generate a Tensor that could as model's input
    
    Usage
    -----
    >>> inp = genModelInput(model)
    >>> result = model(inp)
    >>> tree(result)
    
    Parameters
    ----------
    model: nn.Module
        nn.Module
    inputShape: tuple or list, default None
        By default, inputShape will auto calculate through model's first parameters 
    group: int, default None
        If the first conv has is a group conv, please provide the group num
    ganNoise: bool, default False
        set True, if input is a 1dim vector of noise for GAN
    batchn: int, default 2
        batch number, consider the BatchNorma opr, default of batchn is 2
    """
    inputShape = inputShape or getModelDefaultInputShape(model, group, ganNoise)
    para = getpara(model)
    inp = th.rand((batchn,) + inputShape, dtype=para.dtype, device=para.device)
    if not ganNoise:
        from skimage.data import astronaut

        img = astronaut().mean(-1) / 255.0
        mean = img.mean()
        std = ((img - mean) ** 2).mean() ** 0.5
        normaed = (img - mean) / std
        feat = nn.functional.interpolate(
            tht - [[normaed]], inputShape[-2:], mode="bilinear",
        )
        inp[:] = feat.to(para.device)
    return inp


class HookRegister:
    def __init__(self, module, hook, direct="f"):
        self.hook = hook
        self.hooks = hooks = []
        self.module = module

        def apply(module):
            if direct == "f":
                hooks.append(module.register_forward_hook(hook))
            elif direct == "b":
                hooks.append(module.register_backward_hook(hook))

        module.apply(apply)

    def remove(self):
        for h in self.hooks:
            h.remove()

    def __enter__(self):
        return self

    def __exit__(self, *l):
        self.remove()


def removeAllHook(module):
    def apply(module):
        module._forward_hooks = OrderedDict()

    module.apply(apply)


from boxx import log, ylimgTool, g

ar = FunAddMagicMethod(lambda x: log - ylimgTool.prettyArray(x))


def nanDete(t, globalg=False):
    nan = th.isnan(t).sum()
    if nan:
        if globalg:
            g(1)
        ar(t)
        raise LookupError("Has torch.nan")


def getpara(m):
    """get first parameter"""
    return nextiter(m.parameters())


def getpara0(m):
    return getpara(m).view(-1)[0]


def getgrad(m):
    return getpara(m).grad


def getgrad0(m):
    grad = getpara(m).grad
    return None if grad is None else grad.view(-1)[0]


getpara, getpara0, getgrad, getgrad0 = map(
    FunAddMagicMethod, [getpara, getpara0, getgrad, getgrad0]
)


def get_loss(model_output):
    if isinstance(model_output, (list, tuple)):
        loss = sum([i.sum() for i in model_output])
        return loss
    if isinstance(model_output, dict):
        loss = sum([i.sum() for i in model_output.values()])
        return loss
    return model_output.sum()


def vizmodel(m, inputShape=None, group=None, ganNoise=False, batchn=2, output=""):
    x = genModelInput(
        m, inputShape=inputShape, group=group, ganNoise=ganNoise, batchn=batchn
    )
    from torchviz import make_dot

    x.to(getpara(m))
    model_output = m(x)
    loss = get_loss(model_output)
    graph = make_dot(loss, params=dict(m.named_parameters()))
    if output:
        graph.render(output, format="png")
    return graph


def flatten(t, dim=-1):
    """
    >>> t = shape(1,2,3,4) 
    >>> flatten(t, dim=-2)
    shape(1,6,4)
    """
    shape = list(t.shape)
    shape[dim - 1] *= shape[dim]
    shape.pop(dim)
    return t.reshape(tuple(shape))


def hasnan(tensor):
    return not bool(torch.isfinite(tensor).all())


def pthnan(pth="/home/dl/github/maskrcnn/output/mix_11/model_final.pth"):
    dic = torch.load(pth)
    from collections import OrderedDict

    def getOrderedDict(seq):
        if isinstance(seq, OrderedDict):
            return seq
        if isinstance(seq, dict):
            seq = list(seq.values())
        if not isinstance(seq, (tuple, list)):
            return None
        for s in seq:
            re = getOrderedDict(s)
            if re is not None:
                return re

    od = getOrderedDict(dic)
    tensor = list(od.values())[-1]
    print('"%s"has nan: %s' % (tensor[..., :10], hasnan(tensor)))


if __name__ == "__main__":
    l = [
        "LongTensor",
        "DoubleTensor",
        "IntTensor",
        "ShortTensor",
        "ByteTensor",
        "HalfTensor",
        "CharTensor",
        "FloatTensor",
    ]
    formatt = "th.cuda.%s = th.%s"
    print("\n".join([formatt % (i, i) for i in l]))
