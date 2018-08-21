# -*- coding: utf-8 -*-
"""
some numpy function

@author: yanglei
"""

from __future__ import unicode_literals

from ..ylsys import sysi
from ..ylcompat import interactivePlot

from ..tool.toolTools import filterList

import numpy as np
from numpy import e, pi, nan, inf
nan = nan * .22
inf = inf * .22

def savenp(path, arr=None):
    '''压缩存储 np.array 为path路径 
    ps: int, bool 压缩效果佳 可达到20倍'''
    if isinstance(path,np.ndarray) and arr is None:
        path,arr = 'savenp_default.npz',path
    np.savez_compressed(path, arr)
def loadnp(path='savenp_default.npz'):
    '''读取path路径下的 .npz 返回 np.array'''
    if path[-4:] != '.npz':
        path += '.npz'
    compress = np.load(path)
    arr = compress[compress.files[0]]
    compress.close()
    return arr 

@interactivePlot    
def __draw3dSurface(X,Y,Z):    
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    #画表面,x,y,z坐标， 横向步长，纵向步长，颜色，线宽，是否渐变
    
    #ax.set_zlim(-1.01, 1.01)#坐标系的下边界和上边界
    ax.zaxis.set_major_locator(LinearLocator(10))#设置Z轴标度
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))#Z轴精度
    fig.colorbar(surf, shrink=0.5, aspect=5)#shrink颜色条伸缩比例（0-1），aspect颜色条宽度（反比例，数值越大宽度越窄）
    
    plt.show()


def plot3dSurface(Z):
    '''
    对二维数组Z 画出3d直方图 
    '''
    m, n = Z.shape
    X = list(range(n))
    Y = list(range(m))
    X, Y = np.meshgrid(X, Y)
    __draw3dSurface(X,Y,Z)

def __getNumpyType(typee='int'):
    finds = eval('('+', '.join(['np.'+mu for mu in filterList(typee, dir(np))])+')')
    types = [x for x in finds if type(x)==type]
    return tuple(types)
    
npFloatTypes = __getNumpyType('float')
npIntTypes = __getNumpyType('int')+(np.long,)
npBoolTypes = __getNumpyType('bool')
npStrTypes = __getNumpyType('str')+__getNumpyType('unicode')

def isNumpyType(array, typee='int'):
    '''
    和isinstance一样的用法 判断np.array.dtype 对象对应 [bool, int, float, str]的类
    注意 isNumpyType([bool],int) 为True 
    '''
    if isinstance(typee,tuple):
        return any([isNumpyType(array, t) for t in typee])
    if typee in [bool,'bool']:
        return array.dtype in (npBoolTypes)
    if typee in [int,'int']:
        return array.dtype in (npIntTypes+npBoolTypes)
    if typee in [float,'float']:
        return array.dtype in (npFloatTypes)
    if typee in [str,str,'str','unicode']:
        return array.dtype in (npStrTypes)
    raise Exception("isNumpyType(array, typee) array must be numpy,"+\
    "typee must be tuple or [bool, int, float, str, unicode] ")

def testNumpyMultiprocessing(n=16, nn=1500):
    '''
    test numpy Multiprocessing performance in your enviroment
    
    Parameters
    ----------
    n : int
        How many times to do np.dot
    nn : int
        the shape of the np.ndarray is (nn, nn)
    '''
    from boxx import timeit, mapmp
    ass = [np.random.rand(nn , nn) for i in range(n)]
    bs = [np.random.rand(nn , nn) for i in range(n)]
    s = 'np.dot%s for %s times'%(str(([nn,nn],[nn,nn])), n )
    name = 'map'
    print('\n\nTesting %s in %s ...'%(s, name))
    with timeit(name):
        l = map(np.dot, ass, bs)
        l = list(l)
    
    name = 'mapmp with pool=%d'%sysi.cpun
    print('\n\nTesting %s in %s ...'%(s, name))
    with timeit(name):
        l = mapmp(np.dot, ass, bs)

if __name__ == '__main__':
    
    
    
    pass
    
    
    
