# -*- coding: utf-8 -*-

from __future__ import unicode_literals

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
    ziped = zip(*[iter(listt)]*batch)
    if left:
        ziped.append(tail)
    return ziped

CALL_CLASS_CACHE={}
def addCall(instance):
    '''
    给可以被自己init 的 instance增加__call__ 返回自己
    '''
    t = type(instance)
    if t not in CALL_CLASS_CACHE:
        class T(t):
            def __call__(self):
                return self
        CALL_CLASS_CACHE[t]=T
    return CALL_CLASS_CACHE[t](instance)

class FunAddMagicMethodCore(dict):
    '''magic 未解之谜 疑惑
    >>> z=FunAddMagicMethod(zip)
    >>> isinstance(z,type(zip)) => True
    >>> isinstance(z,dict) => True
    '''
    def __init__(self, fun, returnArg=False):
        self[0] = fun
        self[1] = returnArg
    def __call__(self, *args, **kv):
        resoult = self[0]( *args, **kv)
        if self[1] and len(args)==1:
            return args[0]
        return resoult
    def __div__(self, *args, **kv):
        self[0]( *args, **kv)
        if len(args)==1:
            return args[0]
        return args
    __sub__ = __call__
    __add__ = __call__
    __mul__ = __call__
#    __eq__ = __call__
    __pow__ = __call__
    __invert__ = __call__
class FunAddMagicMethod(FunAddMagicMethodCore):
    '''
    将函数变为带有魔法函数 且可以__call__的对象
    fun : 需要增加为魔法对象的函数
    returnArg : 是否返回输入值本身
    self - arg = fun(arg)
    self / arg = fun(arg) return arg
    '''
    def __getattribute__(self, name=None):
        if name in dir(self[0]):
            return self[0].__getattribute__(name)
        return FunAddMagicMethodCore.__getattribute__(self,name)
    
class dicto(dict):
    '''
    类似JavaScript对象的超级字典，可以动态添加属性
    其中 dicto.keys,dicto.values,dicto.items 添加了property
    这个反射机制是试出来的 原理还不清楚
    '''
    def __init__(self, *l, **kv):
        dict.__init__(self,*l,**kv)
    def __getattribute__(self, name=None):
        if name in self:
            return self[name]
        if name in dir(dict):
            return dict.__getattribute__(self,name)
        return self[name]
    def __setattr__(self, name, v):
        if name in dir(dict):
            return dict.__setattr__(self,name,v)
        self[name] = v
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
def dicToObj(dic):  
    '''
    将 dict 转换为易于调用的 Object
    '''
    top = type(u'MyObject'.encode('utf-8'), (object,), dic)  
    seqs = tuple, list, set, frozenset  
    for i, j in dic.items():  
        if isinstance(j, dict):  
            setattr(top, i, dicToObj(j))  
        elif isinstance(j, seqs):  
            setattr(top, i,   
                type(j)(dicToObj(sj) if isinstance(sj, dict) else sj for sj in j))  
        else:  
            setattr(top, i, j)  
    return top  
    
def addCall(x):
    '''
    对一个可用自己进行初始化的对象增加__call__属性
    如: int, str, dict, list
    '''
    class AddCall(type(x)):
        def __call__(self,*l,**kv):
            if len(l)+len(kv):
                return type(x).__call__(self,*l,**kv)
            return self
    return AddCall(x)

if __name__ == "__main__":

    pass