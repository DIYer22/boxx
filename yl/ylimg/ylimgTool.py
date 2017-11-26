# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from tool.toolStructObj import FunAddMagicMethod
from tool.toolLog import colorFormat
from tool.toolFuncation import mapmp

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import cv2
import skimage as sk
from skimage import io as sio
from skimage import data as da
from skimage.io import imread
from skimage.io import imsave
from skimage.transform import resize 

# randomm((m, n), max) => m*n matrix
# randomm(n, max) => n*n matrix
randomm = lambda shape,maxx:(np.random.random(
shape if (isinstance(shape,tuple) or isinstance(shape,list)
)else (shape,shape))*maxx).astype(int)
r = randomm(4,4)

def normalizing(arr):
    a = arr.astype(float)
    minn = a.min()
    return (a-minn)/(a.max() - minn)
def uint8(img):
    '''将0～1的float或bool值的图片转换为uint8格式'''
    return ((img)*255.999).astype(np.uint8)

greyToRgb = lambda grey:grey.repeat(3).reshape(grey.shape+(3,)) 

npa = FunAddMagicMethod(np.array)


def mapp(f, matrix, need_i_j=False):
    '''
    for each item of a 2-D matrix
    return a new matrix consist of f:f(it) or f(it, i, j)
    性能差 尽量用y, x = np.mgrid[:10,:10]
    '''
    m, n = matrix.shape[:2]
    listt = [[None]*n for i in range(m)]
    for i in range(m):
        for j in range(n):
            it = matrix[i][j]
            listt[i][j] = f(it,i,j) if need_i_j else f(it)
    return np.array(listt)


from operator import add

def ndarrayToImgLists(arr):
    '''
    将所有ndarray转换为imgList
    '''
    arr = np.squeeze(arr)
    ndim = arr.ndim
    if arr.ndim==2 or (arr.ndim ==3 and arr.shape[-1] in [3,4]):
         return [arr]
    if arr.shape[-1] == 2: # 二分类情况下自动转换
        arr = arr.transpose(range(ndim)[:-3]+[ndim-1,ndim-3,ndim-2])
    imgdim = 3 if arr.shape[-1] in [3,4] else 2
    ls = list(arr)
    while ndim-1>imgdim:
        ls = reduce(add,map(list,ls),[])
        ndim -=1
    return ls
def listToImgLists(l, res=None):
    '''
    将 ndarray和list的混合结果树转换为 一维 img list
    '''
    if res is None:
        res = []
    for x in l:
        if isinstance(x,(list,tuple)):
            listToImgLists(x,res)
        if isinstance(x,dict):
            listToImgLists(x.values(),res)
        if isinstance(x,np.ndarray):
            res.extend(ndarrayToImgLists(x))
    return res
def showImgLists(imgs,**kv):
    n = len(imgs)
    if n == 4:
        showImgLists(imgs[:2],**kv)
        showImgLists(imgs[2:],**kv)
        return
    if n > 4:
        showImgLists(imgs[:3],**kv)
        showImgLists(imgs[3:],**kv)
        return 
    fig, axes = plt.subplots(ncols=n)
    count = 0
    axes = [axes] if n==1 else axes 
    for img in imgs:
        axes[count].imshow(img,**kv)
        count += 1
    plt.show()
def show(*imgs,**kv):
    '''
    do plt.imshow to a list of imgs or one img or img in dict or img in np.ndarray
    **kv: args for plt.imshow
    '''
    if 'cmap' not in kv:
        kv['cmap'] = 'gray'
    imgls = listToImgLists(imgs)
    assert len(imgls)!=0,"funcation `show`'s args `imgs`  has no any np.ndarray! "
    showImgLists(imgls,**kv)
show = FunAddMagicMethod(show)


def showb(*arr,**__kv):
    '''
    use shotwell to show picture
    Parameters
    ----------
    arr : np.ndarray or path
    '''
    
    if len(arr)!=1:
        map(lambda ia:showb(ia[1],tag=ia[0]),enumerate(arr))
        return 
    arr = arr[0]
    if isinstance(arr,np.ndarray):
        path = '/tmp/tmp-%s.png'%len(glob.glob('/tmp/tmp-*.png'))
        imsave(path,arr)
        arr = path
    cmd = 'shotwell "%s" &'%arr
    os.system(cmd)
showb = FunAddMagicMethod(showb)

def shows(*imgs):
    '''图片展示分析工具  使用浏览器同步显示同一图像的不同数据表示 如不同通道的image,gt,resoult 
    支持放大缩小与拖拽
    
    Parameters
    ----------
    imgs : list include path or np.ndarray 
        图片地址或图片np.ndarray 组成的list 要求所有图片宽高相同
    '''
    def listToPathList(l, res=None):
        if res is None:
            res = []
        for x in l:
            if isinstance(x,(list,tuple)):
                listToPathList(x,res)
            if isinstance(x,dict):
                listToPathList(x.values(),res)
            if isinstance(x,(str,unicode)):
                res.append(x)
            if isinstance(x,np.ndarray):
                path = '/tmp/shows-%s.png'%len(glob.glob('/tmp/shows-*.png'))
                imsave(path,x)
                res.append(path)
        return res
    paths = listToPathList(imgs)
    from showImgsInBrowser import showImgsInBrowser
    showImgsInBrowser(paths)
shows = FunAddMagicMethod(shows)

def loga(array):
    '''
    Analysis np.array with a graph. include shape, max, min, distribute
    '''
    if isinstance(array,str) or isinstance(array,unicode):
        print 'info and histogram of',array
        l=[]
        eval('l.append('+array+')')
        array = l[0]
    if isinstance(array,list):
        array = np.array(array)
    print 'shape:%s ,type:%s ,max: %s, min: %s'%(str(array.shape),array.dtype.type, str(array.max()),str(array.min()))
    
    unique = np.unique(array)
    if len(unique)<10:
        dic=dict([(i*1,0) for i in unique])
        for i in array.ravel():
            dic[i] += 1
        listt = dic.items()
        listt.sort(key=lambda x:x[0])
        data,x=[v for k,v in listt],np.array([k for k,v in listt]).astype(float)
        if len(x) == 1:
            print 'All value is',x[0]
            return
        width = (x[0]-x[1])*0.7
        x -=  (x[0]-x[1])*0.35
    else:
        data, x = np.histogram(array.ravel(),8)
        x=x[1:]
        width = (x[0]-x[1])
    plt.plot(x, data, color = 'orange')
    plt.bar(x, data,width = width, alpha = 0.5, color = 'b')
    plt.show()
    return 

loga = FunAddMagicMethod(loga)


    
__logFuns = {
 list:lambda x:colorFormat.b%('list  %d'%len(x)),
 tuple:lambda x:colorFormat.b%('tuple %d'%len(x)),
 dict:lambda x:colorFormat.b%('dict  %s'%len(x)),
 np.ndarray:lambda x:colorFormat.r%('%s%s'%
                                    (unicode(x.shape).replace('L,','').replace('L',''),x.dtype)),
 }

def tree(seq,le=None,k=u'/',islast=None):
    '''
    类似bash中的tree命令 简单查看list, tuple, dict, numpy组成的树的每一层结构
    可迭代部分用蓝色 叶子用红色打印
    >>>tree(seq) 
    
    Parameters
    ----------
    seq : list or tuple or dict or numpy or any Object
        打印出 以树结构展开所有可迭代部分
    '''
    if le is None:
        le = [] 
        islast = 1
    s = __logFuns.get(type(seq),lambda x:colorFormat.r%unicode(x)[:60])(seq)
#    print ''.join(le)+u'├── '+unicode(k)+': '+s
    print u'%s%s %s: %s'%(u''.join(le), u'└──' if islast else u'├──',unicode(k),s)
    if isinstance(seq,(list,tuple)):
        seq = list(enumerate(seq))
    elif isinstance(seq,(dict)):
        seq = list(seq.items())
    else:
        return 
    le.append(u'    'if islast else u'│   ')
    for i,kv in enumerate(seq):
        k,v = kv
        tree(v,le,k,islast=(i==len(seq)-1))
    le.pop()
tree = FunAddMagicMethod(tree)

def __typee__(x):
    return unicode(type(x)).split("'")[1]

logModFuns = {
 type(os):lambda x:colorFormat.r%(__typee__(x)),
 }
logMod = lambda mod:logModFuns.get(type(mod),lambda x:colorFormat.b%unicode(__typee__(x))[:60])(mod)
def treem(mod,types=None,deep=None,__leftStrs=None,__name=u'/',islast=None,deepNow=0,rootDir=None,sets=None):
    '''
    类似bash中的tree命令 查看module及子module的每一层结构
    一目了然module的结构和api
    module用红色显示 其余部分用蓝色显示
    >>>treem(os)
    
    Parameters
    ----------
    mod : module
        显示出 以树结构展开module及其子module
        type(mod) should => module
    types : list of types, default None
        需要显示出来的类型(module 类型会自动添加)
        默认显示所有类型
    deep : int, default None
        能显示的最深深度
        默认不限制
    '''
    if deep and deepNow > deep:
        return
    if __leftStrs is None:
        __leftStrs = [] 
        islast = 1
        if '__file__' not in dir(mod): 
            print 'type(%s: %s) is not module!'%(logMod(mod),unicode(mod))
            return 
        rootDir = os.path.dirname(mod.__file__)
        sets = set()
    typeStr = logMod(mod)
    modKinds = ['','','(not sub-module)','(printed befor)']
    modKind = 0
    if isinstance(mod,type(os)):
        if '__name__' in dir(mod) :
            __name = mod.__name__
        modKind = 1
        dirMod = dir(mod)
        if  mod in sets:
            modKind = 3 
        elif '__file__' not in dir(mod) or rootDir not in mod.__file__:
            modKind = 2
    names = (unicode(__name)+('   ' if modKind<2 else u'  ·' )*20)[:40]+modKinds[modKind]
    
    print u'%s%s %s: %s'%(u''.join(__leftStrs), u'└──' if islast else u'├──',typeStr,names)
    
    if modKind !=1:
        return
    sets.add(mod)
    dirMod = [i for i in dirMod if i not in ['__name__','__file__','unicode_literals']]
    if types is not None:
        dirMod=[i for i in dirMod if type(mod.__getattribute__(i)) in  list(types)+[type(os)]] 
    __leftStrs.append(u'    'if islast else u'│   ')
    for i,name in enumerate(dirMod):
        e = mod.__getattribute__(name)
        treem(e,types,deep,__leftStrs,name,islast=(i==len(dirMod)-1),deepNow=deepNow+1,rootDir=rootDir,sets=sets)
    __leftStrs.pop()
treem = FunAddMagicMethod(treem)

def __readShape(n):
    return imread(n).shape
def getShapes(imgGlob, returnn=False):
    '''
    以多线程获得匹配imgGlob的所有图片的shapes
    并print出shapes的最大最小值
    
    Parameters
    ----------
    imgGlob : str
        图片的匹配路径
        如 "/img_data/*.png"
    returnn : bool ,default False
        默认不返回shapes
        为True，则返回shapes
    '''
    names = glob.glob(imgGlob)
    shapes = mapmp(__readShape,names)
    lens = list(map(len,shapes))
    dims = np.unique(lens)
    arr = shapes
    print 'Dims:'
    for dim in dims:
        print '\t %s dim: %d'%(dim,lens.count(dim))
    if len(dims)!=1:
        maxx = max(dims)
        arr=map(lambda s:s+(-1,)*(maxx-len(s)),shapes)
    arr=np.array(arr)
    maxx, minn = [],[]
    for dim in range(max(dims)):
        a = arr[:,dim]
        maxx.append(a[a!=-1].max())
        minn.append(a[a!=-1].min())
    
    print 'Shape:\n \t max shape: %s\n \t min shape: %s'%(maxx,minn)
    if returnn:
        return shapes

def labelToColor(label,colors):
    '''
    将颜色映射到label上
    '''
    colors = np.array(colors)
    if 1.1>(colors).max()>0:
        colors = uint8(colors)
    rgb = np.zeros(label.shape+(3,), np.uint8)
    for c in np.unique(label):
        rgb[label==c] = colors[int(c)]
    return rgb

def standImg(img):
    '''
    任何输入img都转换为 shape is (m, n, 3) dtype == Float
    '''
    from ylnp import isNumpyType
    if img.ndim == 2:
        img = greyToRgb(img)
    if img.dtype == np.uint8:
        img = img/255.
    if isNumpyType(img, bool):
        img = img*1.0
    if isNumpyType(img, float):
        return img
    
def generateBigImgForPaper(imgMa,lengh=1980,border=20,saveName='bigImgForPaper.png'):
    '''
    生成科研写作用的样本对比图
    imgMa: 图片行程的二维列表
    lengh: 大图片的宽度, 长度根据imgMa矩阵的高自动算出
    border: 图片与图片间的间隔
    '''
    big = None
    for rr in imgMa:
        rr = map(standImg,rr)
        nn = len(rr)
        a = int((lengh-nn*border)/nn)
        m,n = rr[0].shape[:2]
        b = int(a*m/n)
        row = None
        rr = [resize(r,(b,a)) for r in rr]
        for r in rr:

            if row is None:
                row = r
            else:
                row = np.append(row,np.ones((b,border,3)),1)
                row = np.append(row,r,1)
        if big is None:
            big = row
        else:
            big = np.append(big,np.ones((border,big.shape[1],3)),0)
            big = np.append(big,row,0)

    show(big)
    if saveName:
        imsave(saveName,big)
    return big
if __name__ == '__main__':

    pass
