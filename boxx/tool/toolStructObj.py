# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from ..ylsys import py2
from ..ylcompat import istype

import inspect
from collections import defaultdict

def listToBatch(listt, batch):
    '''
    将一段序列按照每batch个元素组成一组
    
    >>> listToBatch(range(8),3)
    [(0, 1, 2), (3, 4, 5), (6, 7)]
    '''
    n = len(listt)
    left = n % batch
    if left:
        ind  = n - left
        listt, tail = listt[:ind], tuple(listt[ind:])
    ziped = list(zip(*[iter(listt)]*batch))
    if left:
        ziped.append(tail)
    return ziped

class Ll(list):
    '''
    a tool for convenient list operate
    
    1. quick exec `list(range(int))` buy ll*int:
    >>> ll*4
    [0, 1, 2, 3] 
    
    2. `ll-Iterable`, `ll/Iterable` is a convenient way to exec `list(Iterable)`
    '''
    def __init__(self):
        list.__init__(self, [0, 1])
    def __sub__(self, intOrLazyIter):
        if isinstance(intOrLazyIter, int):
            return self * intOrLazyIter
        return list(intOrLazyIter)
    def __mul__(self, intt):
        return list(range(intt))
    __call__ = __truediv__ = __div__ = __sub__
ll = Ll()

CALL_CLASS_CACHE={}
def addCall(instance):
    '''
    instance增加__call__ 返回自己
    '''
    t = type(instance)
    if t not in CALL_CLASS_CACHE:
        class T(t):
            def __call__(self):
                return self
        CALL_CLASS_CACHE[t]=T
    return CALL_CLASS_CACHE[t](instance)


fun_add_magic_paras = defaultdict(lambda :{})
class FunAddMagicMethodCore(object):
    '''magic 未解之谜 疑惑
    
    >>> z=FunAddMagicMethod(zip)
    >>> isinstance(z,type(zip)) => True
    >>> isinstance(z,object) => True
    '''
    def __init__(self, fun, returnArg=False):
        fun_add_magic_paras[id(self)]['fun'] = fun
        fun_add_magic_paras[id(self)]['returnArg'] = returnArg
    def __call__(self, *args, **kv):
        resoult = fun_add_magic_paras[id(self)]['fun']( *args, **kv)
        if fun_add_magic_paras[id(self)]['returnArg'] and len(args)==1:
            return args[0]
        return resoult
    __sub__ = __call__
    __mul__ = __call__
    __pow__ = __call__
#    __add__ = __call__
#    __eq__ = __call__
#    __invert__ = __call__
    def __div__(self, *args, **kv):
        fun_add_magic_paras[id(self)]['fun']( *args, **kv)
        if len(args)==1:
            return args[0]
        return args
    __truediv__ = __div__
    def __str__(self):
        return 'FunAddMagicMethod(%s)'%fun_add_magic_paras[id(self)]['fun']
    __repr__ = __str__
class FunAddMagicMethod(FunAddMagicMethodCore):
    '''
    add magic method to any callable instance or types,
    then you can call they buy sub, mul, pow operator to call they conveniently
    
    >>> from math import sqrt
    >>> magic_sqrt = mf - sqrt
    >>> (magic_sqrt-9, magic_sqrt*9, magic_sqrt**9) 
    (3.0, 3.0, 3.0)
    
    >>> magic_sqrt/9
    9
    
    the div operator is speacial, cause use div will return arg self
    
    magic_fun (- | * | **) arg => return fun(arg) 
    
    magic_fun / arg = exec fun(arg) but return arg itself
    
    
    
    将函数变为带有魔法函数 且可以__call__的对象
    fun : 需要增加为魔法对象的函数
    self - arg = fun(arg)
    self / arg = fun(arg) return arg
    '''
    def __getattribute__(self, name=None, *l):
        fun = fun_add_magic_paras[id(self)]['fun']
#        from boxx import gg, tree
        if name in dir(fun):
#            tree-[gg.n/name ,gg.f/fun, gg.l/l]
            return getattr(fun,name, *l)
        return FunAddMagicMethodCore.__getattribute__(self, name, *l)
mf = FunAddMagicMethod(FunAddMagicMethod)

class dicto(dict):
    '''
    a subclass of dict for convenient, like object in JavaScript
    
    >>> d = dicto(a=0)
    >>> d.b = 1
    >>> print(d)
    {'a': 0, 'b': 1}
    
    类似 JavaScript 对象的超级字典，可以动态添加属性
    其中 dicto.keys,dicto.values,dicto.items 添加了property
    这个反射机制是试出来的 原理还不清楚
    '''
    def __init__(self, *l, **kv):
        dict.__init__(self,*l,**kv)
    def __getattribute__(self, name=None):
        if name in dir(dict):
            return dict.__getattribute__(self,name)
        if name in self:
            return self[name]
        return self[name]
    def __setattr__(self, name, v):
        if name in dir(dict):
            return dict.__setattr__(self,name,v)
        self[name] = v
    if py2:
        @property
        def keys(self):
            return addCall(dict.keys(self))
        @property
        def values(self):
            return addCall(dict.values(self))
        @property
        def items(self):
            return addCall(dict.items(self))
SuperDict = dicto

def _yield():
    yield 0
generator = type(_yield())

def dicToObj(dic):  
    '''
    将 dict 转换为易于调用的 Object
    '''
    top = type('MyObject'.encode('utf-8'), (object,), dic)  
    seqs = tuple, list, set, frozenset  
    for i, j in list(dic.items()):  
        if isinstance(j, dict):  
            setattr(top, i, dicToObj(j))  
        elif isinstance(j, seqs):  
            setattr(top, i,   
                type(j)(dicToObj(sj) if isinstance(sj, dict) else sj for sj in j))  
        else:  
            setattr(top, i, j)  
    return top  
    

def typeNameOf(classOrType):
    '''
    以str 返回classOrType的所属类别  
    
    >>> typeNameOf(dict) 
    u'dict'
    '''
    ss = str(classOrType).split("'")
    if len(ss)>=3:
        return ss[-2]
    return str(classOrType)

def typestr(instance):
    '''
    以str 返回instance的所属类别  
    
    >>> typestr({}) 
    u'dict'
    '''
    return typeNameOf(type(instance))


def nextiter(iterr, raiseException=True):
    '''
    do next(iter(iterAble)) then return resoult
    
    while iterr is empty and raiseException is False, just return  '【Iterable is empty!】'
    '''
    re = default = '【Iterable is empty!】'
    for i in iterr:
        re = i
        break
    if raiseException and re is default:
        raise StopIteration('Iterable is empty!')
    return re
nextiter = FunAddMagicMethod(nextiter)

def getfathers(objOrType):
    '''
    获得 objOrType 的所有父类，以 tuple 返回
    
    Parameters
    ----------
    objOrType : obj or type (includ classobj in python 2)
        if is obj, 则自动转换为 type(obj)
    '''
    if not istype(objOrType):
        objOrType = type(objOrType)
    return inspect.getmro((objOrType))
getfathers = FunAddMagicMethod(getfathers)

def getfather(objOrType): 
    '''
    获得 objOrType 的父类
    
    Parameters
    ----------
    objOrType : obj or type (includ classobj in python 2)
        if is obj, 则自动转换为 type(obj)
    '''
    return getfathers(objOrType)[0]
getfather = FunAddMagicMethod(getfather)

    
typestr = FunAddMagicMethod(typestr)
if __name__ == "__main__":

    pass