# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time

def getFunName(fun):
    '''
    获得函数的名称
    '''
    if '__name__' in dir(fun):
        return fun.__name__
    return '[unkonw]'

def dynamicWraps(func):
    '''
    decorator 动态规划 装饰器
    '''
    cache={}
    from functools import wraps
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args]=func(*args)
        return cache[args]
    return wrap

    
def setTimeOut(fun, t=0):
    '''
    same to setTimeOut in JavaScript
    '''
    from threading import Timer
    thread = Timer(t,fun)
    thread.start()
    return thread

def setInterval(fun, inter, maxTimes=None):
    '''
    same to setInterval in JavaScript
    '''
    maxTimes = [maxTimes]
    def interFun(): 
        fun()
        if maxTimes[0] is not None:
            maxTimes[0] -= 1
            if maxTimes[0] <= 0:
                return 
        setTimeOut(interFun, inter)
    interFun()

from multiprocessing import Pool as PoolMp
from multiprocessing.dummy import Pool as PoolThread

def __multiprocessingFun__(args):
    '''
    多线程专用
    '''
    return args[0](*args[1:])
def mapmp(fun, *mapArgList, **kv):
    '''
    Multi Processing Map:多进程版本的map函数
    mapmp(fun, sequence[, sequence, ...], pool=None, thread=False)->list
    >>> re = map(np.add,range(10),range(5,15),pool=8)
    
    Notice
    ----------
    * 多进程中 异常无法精确定位
    * numpy操作 由于指令集优化原因 可能多进程和多线程差不多
    * 多进程中 list, dict等元素会被直接复制，无法改变内部元素
    
    Parameters
    ----------
    fun : function
        *多进程*只支持`def`定义的函数 不能是lambda 和 内部函数 
        否则 PicklingError: Can't pickle 
    *mapArgList : list 
        用于fun的参数list, fun需要N个参数则有N个列表
    pool : int, default None
        进程数目，默认为CPU进程数
    thread : bool, default False
        是否以*多线程*形式替换多进程
    '''
    Pool = PoolMp
    if 'thread' in kv and kv['thread']:
        Pool = PoolThread
    pool = Pool(kv['pool']) if 'pool' in kv and kv['pool'] else Pool()
    re = pool.map(__multiprocessingFun__,zip([fun]*len(mapArgList[0]),*mapArgList))
#    re = pool.map(fun,mapArgList[0])
    pool.close()
    pool.join()
    return re

def mapmt(fun, *mapArgList, **kv):
    '''
    Multi Threading Map:多进线版本的map函数
    '''
    return mapmp(fun, *mapArgList,thread=True, **kv)

class multiThread():
    '''
    将多线程封装成为类的形式
    
    Example
    ----------
    >>> mt = multiThread(pool=8)
    >>> for arg in args:
            mt(f,*arg)
    >>> mt.join()
    
    Init Parameters
    ----------
    pool : int, default 8
        线程池的最大线程数目
        
    Method
    ----------
    __call__(fun,*l,**kv):
        fun : 需要多线程的函数 
        *l,**kv : 传给函数的参数们
        新建一个线程 并运行fun(*l,**kv)
    join(): 
        等待至所有线程中止。阻塞主线程直至没有子线程运行。 
    '''
    TIME_GAP = .001
    def __init__(self,pool=8):
        self.pool = pool
        self.left = pool
        self.l=[]
    def __call__(self,fun,*l,**kv):
        while not self.left:
            time.sleep(self.TIME_GAP)
        self.left -=1
        def f():
            try:
                r = fun(*l,**kv)
            finally:
                self.left += 1
        self.l.append(setTimeOut(f))
        if len(self.l)>100:
            self.l = self.l[-90:]
    f = lambda fun,*l,**kv:fun(*l,**kv) #用于测试单线程的性能
    def join(self):
        while self.left!=self.pool:
            time.sleep(self.TIME_GAP)
#        print('pool',self.pool)
if __name__ == "__main__":
    
    def fun():
        for i in range(10):
            print i
            time.sleep(1)
    from threading import Timer
    thread = Timer(0,fun)
    thread.start()
    pass