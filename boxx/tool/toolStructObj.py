# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from ..ylsys import py2
from ..ylcompat import istype

import sys
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

class _SliceToInt():
    ''' convert float to int when in slice
    >>> range(5)[sliceInt[3.3]]
    3
    
    >>> range(5)[sliceInt[-0.1: 3.3]]
    range(0, 3)
    '''
    def intround(self, v):
        if v is None:
            return v
        return int(round(v))
    def __intSlice(self, s):
        intround = self.intround
        return slice(intround(s.start), intround(s.stop), intround(s.step),)
    def __getitem__(self, index):
        def f(t):
            if isinstance(t, tuple):
                return tuple(f(i) for i in t)
            else:
                if isinstance(t, slice):
                    return self.__intSlice(t)
                if isinstance(t, float):
                    return int(round(t))
                return t
        if isinstance(index, (tuple, slice)):
            return f(index)
        return int(round(index))
    @staticmethod
    def test():
        print(range(5)[sliceInt[3.3]])
        print(range(5)[sliceInt[3.3:]])
sliceInt = _SliceToInt()

class sliceLimit():
    ''' limit the value in slice by given numpy array
    
    >>> rr = np.zeros((4,4,4))
    >>> sliceLimit(rr)[-1:2, :1000]
    r[0:2, :4, :]
    
    >>> sliceLimit(rr, True)[-1:2, :1000]
    (slice(0, 2, None), slice(None, 4, None))
    
    >>> sliceLimit(rr, True)[-1:2, ..., :1000]
    (slice(0, 2, None), Ellipsis, slice(None, 4, None))
    '''
    def __init__(self, arr, returnSlice=False):
        self.arr = arr
        self.shape = arr.shape
        self.returnSlice = returnSlice
    def getitem(self, index):
        shape = self.shape
        def sliceTupleLimit(slicee, maxx):
            if not isinstance(slicee, slice):
                return slicee
            return slice(
                    None if slicee.start is None else max(0, slicee.start), 
                    None if slicee.stop is None else min(maxx, slicee.stop), 
                    slicee.step)
        if isinstance(index, slice):
            return sliceTupleLimit(index, shape[0])
        if isinstance(index, tuple):
            splitInd = index.index(Ellipsis) if Ellipsis in index else len(index)
            left = tuple(sliceTupleLimit(slicee, n)  for slicee, n  in zip(index[:splitInd], shape))    
            right = tuple(sliceTupleLimit(slicee, n)  for slicee, n  in zip(index[splitInd+1:][::-1], shape[::-1]))[::-1]
            middle = (Ellipsis,) if Ellipsis in index else ()
            return left + middle + right
        return index
    def __getitem__(self, index):
        new_index = self.getitem(index)
        if self.returnSlice:
            return new_index
        return self.arr[new_index]
    @staticmethod
    def test():
        import numpy as np
        rr = np.zeros((4,4,4))
        print(sliceLimit(rr, True)[-1:2, :1000])
        print(sliceLimit(rr, True)[-3:80, ..., -3:80])

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
        if name in ['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__div__', '__doc__', '__eq__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__mul__', '__ne__', '__new__', '__pow__', '__reduce__', '__repr__', '__setattr__', '__str__', '__sub__', '__truediv__']:
            return FunAddMagicMethodCore.__getattribute__(self, name, *l)
        return getattr(fun,name, *l)
mf = FunAddMagicMethod(FunAddMagicMethod)

# invalid a function
fnone = mf(lambda *l, **kv: l[0] if len(l)==1 else l)

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
        return None
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
typestr = FunAddMagicMethod(typestr)

def strMethodForDiraAttrs(self, pattern='^[^_]'):
    '''
    the default of __str__ method in Class
    
    will return string of dira(self) 
    
    '''
    from boxx import dira, PrintStrCollect
    printf = PrintStrCollect()
    dira(self, pattern=pattern, printf=printf, printClassFathers=False)
    s = str(printf)
    if py2:
        s = s[s.index(u'└'.encode('utf-8')):]
        return s
    s = s[s.index('└'):]
    return s

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
    

def setself(self=None):
    '''
    set all method(*args)  to self.__dict__ 
    
    >>> class A():
    ...     def __init__(self, attr='attr'):
    ...         setself()
    >>> a=A()
    >>> a.attr
    'attr'
    '''
    local = sys._getframe(1).f_locals
    if self is None:
        self = local['self']
    self.__dict__.update(local)
#    tree-local

def unfoldself(self=None):
    '''
    set all self.__dict__ to locals()
    
    >>> class A():
    ...     def __init__(self):
    ...         self.attr='attr'
    ...     def get_attr(self):
    ...         unfoldself()
    ...         return attr
    >>> a=A()
    >>> a.get_attr()
    'attr'
    
    ps. if vars name in locals(), the vars won't be cover
    '''
    local = sys._getframe(1).f_locals
    if self is None:
        self = local['self']
    for k, v in self.__dict__.items():
        if k not in local:
            local[k] = v

class withfun():
    '''
    Convenient way to use `with statement` without build a Class
    enterFun and exitFun are no parameter function
    
    Parameters
    ----------
    enterFun : function, default None
        No parameter function
    exitFun : function, default None
        No parameter function or parameter are (exc_type, exc_value, exc_traceback)
    exception : bool, default False
        Whether send (exc_type, exc_value, exc_traceback) to exitFun
    '''
    def __init__(self, enterFun=None, exitFun=None, exception=False):
        self.enterFun = enterFun
        self.exitFun = exitFun
        self.exception = exception
    def __enter__(self):
        if self.enterFun:
            return self.enterFun()
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.exitFun:
            if self.exception:
                self.exitFun(exc_type, exc_value, exc_traceback)
            else:
                self.exitFun()

class withattr(withfun):
    '''
    set attr or item in `with statement`, after __exit__ the obj or dict will recovery like befor 
    
    Parameters
    ----------
    obj : obj or dict
        the thing that will change attr or item in with statement
    attrs : dict
        the attrs or items that will change during with statement
    
    Usage
    ----------
    
    >>> with withattr(dict(), {'attr':'value'}) as d:
    ...     print(d['attr'])
    value
    >>> 'attr' in d
    False
    
    ps. `withattr` will detecat whther the obj is dict, then choose setattr or setitem.
    '''
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
            return d
        def exitFun():
            for k in attrs.keys():
                pop(d, k)
            if isinstance(d, dict):
                d.update(self.old)
            else:
                for k, v in self.old.items():
                    sett(d, k, v)
        withfun.__init__(self,enterFun, exitFun)
    
def isinstancestr(obj, typeStrList):
    '''
    same as isinstance but only use type name strs to avoid `import torch.tensor` .etc
    
    Parameters
    ----------
    obj : object
        anything
    typeStrList : str or list of strs
        like tuple of types for isinstance
    
    Return
    ----------
    if True return the type name str
    '''
    if isinstance(typeStrList, str):
        typeStrList = [typeStrList]
    types = getfathers(obj)
    typestrs = list(map(typeNameOf, types))
    for t in typeStrList:
        if t in typestrs:
            typestrs.index(t)
            return t
    return False

if __name__ == "__main__":

    pass