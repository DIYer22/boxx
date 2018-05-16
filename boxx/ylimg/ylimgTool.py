# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from ..tool.toolStructObj import FunAddMagicMethod, typeNameOf, typestr, dicto, generator, nextiter, getfathers
from ..tool.toolLog import log, colorFormat, clf, tounicode, LogLoopTime, prettyClassFathers
from ..tool.toolLog import tabstr, getDoc, shortDiscrib, discrib
from ..tool.toolFuncation import mapmp, pipe
from ..tool.toolSystem import tryImport
from ..ylsys import tmpYl
from ..ylnp import isNumpyType

import skimage as sk
from skimage import io as sio
from skimage import data as sda
from skimage.io import imread
from skimage.io import imsave
from skimage.transform import resize 

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import types
from functools import reduce
from collections import defaultdict
from operator import add
#cv2 = tryImport('cv2')

# randomm((m, n), max) => m*n matrix
# randomm(n, max) => n*n matrix
randomm = lambda shape,maxx:(np.random.random(
shape if (isinstance(shape,tuple) or isinstance(shape,list)
)else (shape,shape))*maxx).astype(int)
r = randomm(4,4)

def normalizing(arr):
    if isinstance(arr, np.ndarray) and not isNumpyType(arr, 'float'):
        arr = arr.astype(float)
    minn = arr.min()
    return (arr-minn)/(arr.max() - minn)
normalizing = FunAddMagicMethod(normalizing)
norma = normalizing

def uint8(img):
    '''将0～1的float或bool值的图片转换为uint8格式'''
    return ((img)*255.999).astype(np.uint8)

greyToRgb = lambda grey:grey.repeat(3).reshape(grey.shape+(3,)) 

histEqualize = FunAddMagicMethod(sk.exposure.equalize_hist)

boolToIndex = lambda boolMa1d:np.arange(len(boolMa1d))[npa(boolMa1d).squeeze()>0]
boolToIndex = FunAddMagicMethod(boolToIndex)

def tprgb(ndarray):
    '''
    transpose to RGB, 将3*h*w的ndarray化为 h*w*3的RGB图
    即shape为 (...,3 , h, w)的ndarray转化为(..., h, w, 3)
    '''
    shape = ndarray.shape
    ndim = ndarray.ndim
    if ndim >= 3 and shape[-3] == 3:
        axes = list(range(ndim))[:-3]+[ndim-2,ndim-1,ndim-3]
        return ndarray.transpose(*axes)
    return ndarray
tprgb = FunAddMagicMethod(tprgb)

def torgb(img):
    '''
    将被处理过给网络用的图片 转换回 RGB 图像。
    即自动 Normalization 到 [0,1], 并transpose 到 W*H*3
    '''
    if img.min() < 0:
        img = norma(img)
    return tprgb(img)
torgb = FunAddMagicMethod(torgb)

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

def __torchVar2Tensor(t):
    '''
    同时兼容 PyTorch 3.0 和 4.0 的 Tensor 和 Var
    '''
    try:
        t = t.data
    except:
        pass
    finally:
        return t
__torchToNumpy = lambda x:__torchVar2Tensor(x).numpy()
__torchCudaToNumpy = lambda x:__torchVar2Tensor(x).cpu().numpy()

typesToNumpyFuns = {
    'PIL.Image.Image':lambda x:np.array(x),
    'mxnet.ndarray.NDArray':lambda x:x.asnumpy(),
    
    'torch.Tensor':__torchCudaToNumpy,
    
    'torch.FloatTensor':__torchToNumpy,
    'torch.DoubleTensor':__torchToNumpy,
    'torch.IntTensor':__torchToNumpy,
    'torch.LongTensor':__torchToNumpy,
    'torch.ShortTensor':__torchToNumpy,
    'torch.ByteTensor':__torchToNumpy,
    'torch.HalfTensor':__torchToNumpy,
    'torch.CharTensor':__torchToNumpy,
    
    "torch.cuda.LongTensor":__torchCudaToNumpy,
    "torch.cuda.DoubleTensor":__torchCudaToNumpy,
    "torch.cuda.IntTensor":__torchCudaToNumpy,
    "torch.cuda.ShortTensor":__torchCudaToNumpy,
    "torch.cuda.ByteTensor":__torchCudaToNumpy,
    "torch.cuda.HalfTensor":__torchCudaToNumpy,
    "torch.cuda.CharTensor":__torchCudaToNumpy,
    "torch.cuda.FloatTensor":__torchCudaToNumpy,
    
    "torch.autograd.variable.Variable":lambda x:__torchCudaToNumpy(x.data),
    "torch.nn.parameter.Parameter":lambda x:__torchCudaToNumpy(x.data),
}

__generatorToNumpy = lambda x:np.array(list(x))
tryToNumpyFunsForNpa = {
    "dict_values":__generatorToNumpy,
    "dict_keys":__generatorToNumpy,
    "dict_items":__generatorToNumpy,
    "map":__generatorToNumpy,
    "filter":__generatorToNumpy,
    "zip":__generatorToNumpy,
    }
def npa(array):
    '''
    根据`./typesToNumpyFuns` 将array转换为 np.ndarray
    
    Parameters
    ----------
    array : list/tuple, torch.Tensor, mxnet.NDArray 
        在 字典 typesToNumpyFuns 的中的类型
    '''
    typeName = typestr(array)
    if typeName in tryToNumpyFunsForNpa:
        ndarray = tryToNumpyFunsForNpa[typeName](array)
    elif typeName in typesToNumpyFuns:
        ndarray = typesToNumpyFuns[typeName](array)
    else:
        ndarray = np.array(array)
    return ndarray
npa = FunAddMagicMethod(npa)


def discribArray(array):
    '''
    return str of discrib for array, include shape type max min
    '''
    typeName = typestr(array)
    array = npa(array)
    strr = (clf.r%tounicode(array.shape),
          clf.r%typeNameOf(array.dtype.type)[6:], 
          clf.r%typeName,
          clf.r%( (array.max()) if (array.size) else 'Empty'), 
          clf.r%( (array.min()) if (array.size) else 'Empty') )
    return (('shape:%s type:(%s of %s) max: %s, min: %s'%tuple(strr)))
    
    
def prettyArray(array):
    '''
    return str of pretty discrib for array, include nan inf (shape type max min)  
    '''
    discrib = discribArray(array)
    array = npa(array)
    unique = np.unique(array)
    finiteInd = np.isfinite(array)
    nan = np.isnan(array).sum()
    
    discribNan = ''
    if not (finiteInd).all():
        finite = array[finiteInd]
        size = array.size
        nan = np.isnan(array).sum()
        nans = clf.p%'"nan":%s (%.2f%%), '%(nan,100.*nan/size) if nan else ''
        inf = np.isinf(array).sum()
        infs = clf.p%'"inf":%s (%.2f%%), '%(inf,100.*inf/size) if inf else ''
        discribNan = (clf.r%'\nNotice: ' + '%s%s finite max: %s, finite min: %s'%(nans,infs, len(finite) and (finite.max()), len(finite) and (finite.min())))
    if len(unique)<10:
        dic = defaultdict(lambda : 0)
        for i in array.ravel():
            dic[i] += 1
        listt = list(dic.items())
        listt.sort(key=lambda x:x[0])
        x = np.array([k for k,v in listt]).astype(float)
        if len(x) == 0:
            discrib += (clf.p%'\nEmpty array')
        elif len(x) == 1:
            discrib += (clf.p%'\nAll value is %s' % x[0])
        else:
            discrib += ('\nOlny %s unique values are %s'%(len(x), ', '.join([clf.p%v for v in x])))
    discrib += discribNan
    return discrib

def plot(array, sort=False, maxline=10):
    '''to do
    plot line or lines
    '''
    if callable(array):
        x = np.linspace(np.e*-1.5,np.e*1.5,100)
        array = array(x)
    discrib = prettyArray(array).replace('\n','\n\n')
    print(discrib)
    array = npa(array).squeeze()
    n = array.shape[-1]
    if array.ndim >= 2:
        array = np.resize(array, (array.size//n, n))
        arrays = array[:maxline]
    else:
        arrays = [array]
    for arr in arrays:
        if sort:
            arr = sorted(arr, reverse=True)
        plt.plot(arr)
    plt.show()        
plot = FunAddMagicMethod(plot)
 
def loga(array):
    '''
    Analysis np.array with a graph. include shape, max, min, distribute
    '''
    discrib = prettyArray(array)
    print(discrib.replace('\n','\n\n'))
    
    array = npa(array)
    unique = np.unique(array)
    finiteInd = np.isfinite(array)
    if not (finiteInd).all():
        finite = array[finiteInd]
        data, x = np.histogram(finite,8)
    if len(unique)<10:
        dic = defaultdict(lambda : 0)
        for i in array.ravel():
            dic[i] += 1
        listt = list(dic.items())
        listt.sort(key=lambda x:x[0])
        data,x=[v for k,v in listt],np.array([k for k,v in listt]).astype(float)
        if len(x) <= 1:
            return
        width = (x[0]-x[1])*0.7
        x -=  (x[0]-x[1])*0.35
    elif not (finiteInd).all():
        x=x[1:]
        width = (x[0]-x[1])
    else:
        data, x = np.histogram(array.ravel(),8)
        x=x[1:]
        width = (x[0]-x[1])
    plt.plot(x, data, color = 'orange')
    plt.bar(x, data,width = width, alpha = 0.5, color = 'b')
    plt.show()
    
loga = FunAddMagicMethod(loga)

def ndarrayToImgLists(arr):
    '''
    将所有ndarray转换为imgList
    '''
    arr = np.squeeze(arr)
    ndim = arr.ndim
    if not ndim:
        return []
    if arr.ndim==2 or (arr.ndim ==3 and arr.shape[-1] in [3,4]):
         return [arr]
    if arr.shape[-1] == 2: # 二分类情况下自动转换
        arr = arr.transpose(list(range(ndim))[:-3]+[ndim-1,ndim-3,ndim-2])
    imgdim = 3 if arr.shape[-1] in [3,4] else 2
    ls = list(arr)
    while ndim-1>imgdim:
        ls = reduce(add,list(map(list,ls)),[])
        ndim -=1
    return ls

def listToImgLists(l, res=None,doNumpy=ndarrayToImgLists):
    '''
    将 ndarray和list的混合结果树转换为 一维 img list
    '''
    if res is None:
        res = []
    for x in l:
        typeName = typestr(x)
        fathersStr = str(getfathers(x))
        if typeName in typesToNumpyFuns:
            ndarray = typesToNumpyFuns[typeName](x)
            res.extend(doNumpy(ndarray))
        elif isinstance(x,(list,tuple)):
            listToImgLists(x,res=res,doNumpy=doNumpy)
        elif isinstance(x,dict):
            listToImgLists(list(x.values()),res=res,doNumpy=doNumpy)
        elif isinstance(x,np.ndarray):
            res.extend(doNumpy(x))
        elif ('torch.utils.data') in fathersStr or ('torchvision.datasets') in fathersStr:
            seq = unfoldTorchData(x)
            if seq is not False:
                listToImgLists(seq,res=res,doNumpy=doNumpy)
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
def show(*imgsAndFuns,**kv):
    '''
    找出一个复杂结构中的所有numpy 转换为对应的图片并plt.show()出来
    
    Parameters
    ----------
    imgsAndFuns : list/tuple/dict 
    '''
    if 'cmap' not in kv:
        kv['cmap'] = 'gray'
    funs = [arg for arg in imgsAndFuns[1:] if callable(arg)]
    doNumpy = pipe(funs+[ndarrayToImgLists])
    imgls = listToImgLists(imgsAndFuns,doNumpy=doNumpy)
    imgls = [img for img in imgls if img.ndim >= 2 and min(img.shape) > 2]
    assert len(imgls)!=0,"funcation `show`'s args `imgs`  has no any np.ndarray that ndim >= 2! "
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
        list(map(lambda ia:showb(ia[1],tag=ia[0]),enumerate(arr)))
        return 
    arr = arr[0]
    if isinstance(arr,np.ndarray):
        path = tmpYl + 'tmp-%s.png'%len(glob.glob(tmpYl + 'tmp-*.png'))
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
                listToPathList(list(x.values()),res)
            if isinstance(x,str):
                res.append(x)
            if isinstance(x,np.ndarray):
                path = tmpYl + '/shows-%s.png'%len(glob.glob(tmpYl + '/shows-*.png'))
                imsave(path,x)
                res.append(path)
        return res
    paths = listToPathList(imgs)
    from .showImgsInBrowser import showImgsInBrowser
    showImgsInBrowser(paths)
shows = FunAddMagicMethod(shows)



__torchShape = lambda x:colorFormat.r%'%s %s'%(str(x.shape),x.type())
StructLogFuns = {
    'list':lambda x:colorFormat.b%('list  %d'%len(x)),
    'tuple':lambda x:colorFormat.b%('tuple %d'%len(x)),
    'dict':lambda x:colorFormat.b%('dict  %s'%len(x)),
    'set':lambda x:(colorFormat.r%'set %s = '%len(x) + colorFormat.b%str(x)),
    'collections.defaultdict':lambda x:colorFormat.b%('defaultDict  %s'%len(x)),
    'dicto':lambda x:colorFormat.b%('dicto  %s'%len(x)),
    'tool.toolStructObj.dicto':lambda x:colorFormat.b%('dicto  %s'%len(x)),
    'tool.toolLog.SuperG':lambda x:colorFormat.b%('SuperG  %s'%len(x)),
    'collections.OrderedDict':lambda x:colorFormat.b%('OrderedDict  %s'%len(x)),
    'dictoSub':lambda x:colorFormat.b%('dictoSub  %s'%len(x)),
    
    'numpy.ndarray':lambda x:colorFormat.r%('%s%s'%
                                    (str(x.shape).replace('L,','').replace('L',''),x.dtype)),

    'torch.Tensor':__torchShape,
    
    'torch.FloatTensor':__torchShape,
    'torch.DoubleTensor':__torchShape,
    'torch.IntTensor':__torchShape,
    'torch.LongTensor':__torchShape,
    'torch.ShortTensor':__torchShape,
    'torch.ByteTensor':__torchShape,
    'torch.HalfTensor':__torchShape,
    'torch.CharTensor':__torchShape,
    
    "torch.cuda.LongTensor":__torchShape,
    "torch.cuda.DoubleTensor":__torchShape,
    "torch.cuda.IntTensor":__torchShape,
    "torch.cuda.ShortTensor":__torchShape,
    "torch.cuda.ByteTensor":__torchShape,
    "torch.cuda.HalfTensor":__torchShape,
    "torch.cuda.CharTensor":__torchShape,
    "torch.cuda.FloatTensor":__torchShape,
    "torch.autograd.variable.Variable":lambda x:__torchShape(x.data),
    "torch.nn.parameter.Parameter":lambda x:__torchShape(x.data),
    
    'torch.utils.data.dataloader.DataLoader':lambda x:(colorFormat.b%'DataLoader(len=%d, batch=%d, worker=%d)'%
                                                       (len(x.dataset), x.batch_size, x.num_workers)),
    
    'mxnet.ndarray.NDArray':lambda x:'mxnet.NDArray%s'%str(x.shape),
    
    'pandas.core.frame.DataFrame':lambda x:clf.r%'DataFrame(col=%d, Index=[%s], dtype="%s")'%(x.shape[0], ', '.join(map(str,x.columns)), x.columns.dtype)
    }

def discribOfInstance(instance,leafColor=None,MAX_LEN=45):
    typee = type(instance)
    typen = typeNameOf(typee)
#    print typen,typen in StructLogFuns
    if isinstance(instance,dicto) and typen not in StructLogFuns:
        typen = 'dictoSub'
    if typen in StructLogFuns:
        s = StructLogFuns[typen](instance)
        return shortDiscrib(s, MAX_LEN+18)
    s = tounicode(instance)
    if len(s) > MAX_LEN:
        s = s[:MAX_LEN-3]+'...'
    return (leafColor or '%s')%s


def unfoldTorchData(seq):
    '''
    unfold torch.Dataset and Dataloader use next(iter()) for tree  
    '''
    import torch
    if isinstance(seq, torch.utils.data.DataLoader):
        seq = [('DataLoader.next', nextiter(seq, raiseException=False))]
    elif isinstance(seq, torch.utils.data.Dataset):
        seq = [(colorFormat.b%'Dataset[0/%d]'%len(seq), seq[0])]
    else:
        return False
    return seq

def unfoldAble(seq):
    '''
    能展开的 object 
    '''
    if isinstance(seq,(list,tuple,dict,types.GeneratorType)) :
        if isinstance(seq,(list,tuple)):
            seq = list(enumerate(seq))
        elif isinstance(seq,(dict)):
            seq = list(seq.items())
        elif isinstance(seq, types.GeneratorType):
            seq = [('Generator.next', nextiter(seq, raiseException=False))]
        return seq
    fathersStr = str(getfathers(seq))
    if ('torch.utils.data') in fathersStr or ('torchvision.datasets') in fathersStr:
        return unfoldTorchData(seq)
    return False

class HiddenForTree():
    def __init__(self, lenn, maxprint):
        self.n = lenn
        self.m = maxprint
        self.s = colorFormat.r%'Hidden %s of all %d'%((lenn-maxprint//2*2), lenn)
        self.repeat = max(4,min(1,maxprint//2))
    def __str__(self):
        return self.s
    def strr(self, leftStr):
        lineTempl = ''.join(leftStr)
        lineTempl += '├── '
        half = (lineTempl + colorFormat.r%'···\n')*self.repeat
        mid = lineTempl + colorFormat.b%self.s+'\n'
        s = half + mid + half
        return s 
    
def tree(seq,maxprint=50,deep=None,logLen=45,dealStr=log,leafColor='\x1b[31m%s\x1b[0m',__key='/',__leftStr=None, __islast=None,__deepNow=0, __sets=None):
    '''
    类似bash中的tree命令 
    直观地查看list, tuple, dict, numpy, tensor, dataset, dataloader 等组成的树的每一层结构   
    可迭代部分用蓝色 叶子用红色打印   
    以下命令可以查看支持的数据结构类型   
    
    >>> tree(boxx.ylimg.ylimgTool.StructLogFuns)
    
    Parameters
    ----------
    seq : list or tuple or dict or numpy or tensor or torch.Dataset or torch.Dataloader or any Object
        打印出 以树结构展开所有可迭代部分
    maxprint : int, default 50
        每个 seq 内部，最大允许的数目 默认最多展示 50 个   
        若 bool(maxprint) 为 False 则不做限制
    deep : int, default None
        能显示的最深深度, 默认不限制
    logLen : int, default 45
        能显示的最长字符数
    
    ps.可在StructLogFuns中 新增类别
    '''
    if deep and __deepNow > deep:
        return
    if __leftStr is None:
        __leftStr = [] 
        __islast = 1
        __sets = set()
    if maxprint and isinstance(seq, HiddenForTree):
        dealStr(seq.strr(__leftStr), end='')
        return 
#    s = StructLogFuns.get(type(seq),lambda x:colorFormat.r%tounicode(x)[:60])(seq)
    try:
        s = discribOfInstance(seq,leafColor=leafColor,MAX_LEN=logLen)
    except Exception as e:
        s = colorFormat.r%"【%s】"%e.__repr__()
    s = s.replace('\n','↳')
#    dealStr ''.join(__leftStr)+u'├── '+tounicode(k)+': '+s
    dealStr('%s%s %s: %s'%(''.join(__leftStr), '└──' if __islast else '├──',tounicode(__key),s))
    
    unfold = unfoldAble(seq)
    if unfold is False :
        return 
    else:
        if id(seq) in __sets:
            seq=[(colorFormat.p%'【printed befor】','')]
        else:
            __sets.add(id(seq))
            seq = unfold
    __leftStr.append('    'if __islast else '│   ')
    if maxprint : 
        lenn = len(seq)
        if lenn > maxprint:
            head = maxprint//2
            seq = seq[:head] + [('HiddenForTree',HiddenForTree(lenn=lenn, maxprint=maxprint))] + seq[-head:]
    for i,kv in enumerate(seq):
        __key,v = kv
        tree(v,maxprint=maxprint,deep=deep,logLen=logLen, dealStr=dealStr,leafColor=leafColor, __key=__key, __leftStr=__leftStr, 
             __islast=(i==len(seq)-1),__deepNow=__deepNow+1,__sets=__sets)
    __leftStr.pop()
tree = FunAddMagicMethod(tree)

def __typee__(x):
    return tounicode(type(x)).split("'")[1]

logModFuns = {
 type(os):lambda x:colorFormat.r%(__typee__(x)),
 }
logMod = lambda mod:logModFuns.get(type(mod),lambda x:colorFormat.b%tounicode(__typee__(x))[:60])(mod)
def treem(mod, types=None, deep=None, __leftStrs=None, __name='/', 
          __islast=None, __deepNow=0, __rootDir=None, __sets=None):
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
        ps.为了使用deep更简便 若`treem(mod, [int])` 
           则自动转换为`treem(mod, types=None, deep=[int])`
    deep : int, default None
        能显示的最深深度
        默认不限制
    '''
    if isinstance(types, int):
        deep = types
        types = None
    if deep and __deepNow > deep:
        return
    if __leftStrs is None:
        __leftStrs = [] 
        __islast = 1
        if '__file__' not in dir(mod): 
            print('type(%s: %s) is not module!'%(logMod(mod),tounicode(mod)))
            return 
        __rootDir = os.path.dirname(mod.__file__)
        __sets = set()
    typeStr = logMod(mod)
    modKinds = ['','','(not sub-module)','(printed befor)']
    modKind = 0
    if isinstance(mod,type(os)):
        if '__name__' in dir(mod) :
            __name = mod.__name__
        modKind = 1
        dirMod = dir(mod)
        if  mod in __sets:
            modKind = 3 
        elif '__file__' not in dir(mod) or __rootDir not in mod.__file__:
            modKind = 2
    names = (tounicode(__name)+('   ' if modKind<2 else '  ·' )*20)[:40]+modKinds[modKind]
    
    print('%s%s %s: %s'%(''.join(__leftStrs), '└──' if __islast else '├──',typeStr,names))
    
    if modKind !=1:
        return
    __sets.add(mod)
    dirMod = [i for i in dirMod if i not in ['__name__','__file__','unicode_literals']]
    if types is not None:
        dirMod=[i for i in dirMod if type(mod.__getattribute__(i)) in  list(types)+[type(os)]] 
    __leftStrs.append('    'if __islast else '│   ')
    for i,name in enumerate(dirMod):
        e = mod.__getattribute__(name)
        treem(e,types,deep,__leftStrs,name,__islast=(i==len(dirMod)-1),__deepNow=__deepNow+1,__rootDir=__rootDir,__sets=__sets)
    __leftStrs.pop()
treem = FunAddMagicMethod(treem)

def getFunDocForDira(f):
    d = getDoc(f)
    if d:
        return ' : %s'%(colorFormat.black%tounicode(d.strip()))
    return ''

attrLogFuns = {
'method-wrapper': lambda x:'method-wrapper%s'%getFunDocForDira(x),
'builtin_function_or_method':lambda x:'builtin-method%s'%getFunDocForDira(x),
'instancemethod':lambda x:'instancemethod%s'%getFunDocForDira(x),
'buffer':lambda x:'buffer : %s'%(colorFormat.b%tounicode(x)),
}

def __dira(seq,instance=None, maxDocLen=50, deep=None, __leftStr=None,__key='/',__islast=None,__deepNow=0, __sets=None):
    '''
    类似bash中的tree命令 简单查看instance的 __attrs__ 组成的树的结构
    attr name用红色；str(instance.attr)用蓝色；
    如果attr 为instancemethod，builtin_function_or_method，method-wrapper之一
    instance.attr.__doc__用黑色 
    
    ps.可在__attrLogFuns中 新增常见类别
    '''
    if deep and __deepNow > deep:
        return
    s = discribOfInstance(seq,colorFormat.b,MAX_LEN=maxDocLen)
    if maxDocLen < 100:
        s = s.replace('\n','↳')
    if __leftStr is None:
        __leftStr = [] 
        __islast = 1
        __sets = set()
        doc = '' if instance is None else getFunDocForDira(instance)
        if len(doc) > maxDocLen:
            doc = doc[:maxDocLen-3]+'...'
        s=colorFormat.b%('%d attrs%s'%(len(seq), doc.replace('\n','↳').replace(' :',',',1)))
#    print ''.join(__leftStr)+u'├── '+tounicode(k)+': '+s
    print('%s%s %s: %s'%(''.join(__leftStr), '└──' if __islast else '├──',colorFormat.r%tounicode(__key),s))
    if isinstance(seq,(list,tuple,dict)) :
        if id(seq) in __sets:
            seq=[(colorFormat.p%'【printed befor】','')]
        else:
            __sets.add(id(seq))
            if isinstance(seq,(list,tuple)):
                seq = list(enumerate(seq))
            elif isinstance(seq,(dict)):
                seq = list(seq.items())
                try: # key may not be sort
                    seq.sort(key=lambda x:x[0])
                except:
                    pass
    else:
        return 
    __leftStr.append('    'if __islast else '│   ')
    seq =  [(k,filterMethodName(k,v)) for k,v in seq]
    for i,kv in enumerate(seq):
        __key,v = kv
        __dira(v,maxDocLen=maxDocLen,deep=deep,__leftStr=__leftStr,__key=__key,
               __islast=(i==len(seq)-1), __deepNow=__deepNow+1,__sets=__sets)#leafColor=colorFormat.black)
    __leftStr.pop()

def filterMethodName(attrName, attr):
    typee = type(attr)
    typn = typeNameOf(typee)
    if typn in attrLogFuns:
        return attrLogFuns[typn](attr)
    if attrName in ('__globals__', 'func_globals'):
        return colorFormat.b%('【globals-dict %d omitted】'%len(attr))
    elif attrName in ('__builtins__', ):
        return colorFormat.b%('【builtins-dict %d omitted】'%len(attr))
    elif attrName in ('__all__',):
        return colorFormat.b%('【all-list %d omitted】'%len(attr))
    elif attrName == ('f_builtins'):
        return colorFormat.b%('【f_builtins %d omitted】'%len(attr))
    return attr

def dira(instance, pattern=None, deep=None, maxDocLen=50, __printClassFathers=True):
    '''
    以树的结构 分析instance的所有 attrs, 并展示父类的继承链
    attr name用红色；str(instance.attr)用蓝色；
    如果attr 为instancemethod，builtin_function_or_method，method-wrapper之一
    instance.attr.__doc__用黑色 
    
    Parameters
    ----------
    instance : Anything
        Anything, Instance better
    pattern : re.pattern
        用于匹配re.search参数 进行filter
        ps.为了使用deep更简便 若`dira(instance, [int])` 
           则自动转换为`dira(instance, pattern=None, deep=[int])`
    maxDocLen : int, default 50
        若有文档显示文档的字数长度
    deep : int, default None
        能显示的最深深度, 默认不限制
        
    ps.可在__attrLogFuns中 新增常见类别
    pps.不展开 ('__globals__', 'func_globals', __builtins__, __all__, f_builtins)
    '''
    if __printClassFathers:
        s = prettyClassFathers(instance)
        print((colorFormat.b%'Classes: \n'+'└── '+s+''))
    
    print((colorFormat.b%'Attrs: '))
    if isinstance(pattern, int):
        deep = pattern
        pattern = None
    dirs = dir(instance)
    if pattern is not None:
        import re
        dirs = [name for name in dirs if re.search(pattern,name)]
        print('Filter by pattern: "%s"'%(colorFormat.r%pattern))
    def getAttr(attr):
        try:
            try :
                return getattr(instance, attr)
            except :
                pass
            try:
    #            if '__getattribute__' in dirs or 1:
                return instance.__getattribute__(attr)
            except (TypeError): # may be type
                try :
                    return instance.__getattribute__(instance, attr)
                except :
                    pass
                
            except (AttributeError, KeyError):
                pass
            try:
                if '__getattr__' in dirs:
                    return instance.__getattr__(attr)
            except (AttributeError, TypeError):
                return colorFormat.p % '【"getattr"/"getattribute" are not work】'
            return  colorFormat.p % '【No "getattr" or "getattribute"】'
        except Exception as e:
            return colorFormat.p % '【"getAttr" fail, %s(%s)】'%(typestr(e),e)
    l = list(map(getAttr,dirs))
    l = list(map(filterMethodName,dirs,l))
    dic = dict(list(zip(dirs,l)))    
    __dira(dic,instance=instance, maxDocLen=maxDocLen, deep=deep,__key=typeNameOf(type(instance)), )

dira = FunAddMagicMethod(dira)
treea = dira

def what(anything, full=False):
    '''
    tell you what's this by
    pretty print `Document`, `Classes`, `Inner Struct`, `Attributes` of anything.
    
    a magic tool to learn new Python Package

    Parameters
    ----------
    anything : anything in Python
        decompose all of anything
    full : bool, default False
        in default, print lines is less than 10
        set full to True, print all lines
    '''
    tostr = discrib(anything, maxline=not(full) and 10)
    doc = getDoc(anything) or clf.p%"【Not found document】"
    doc = discrib(doc, maxline=not(full) and 15)
    classes = prettyClassFathers(anything)
    
    print('-'*15+clf.b%'end of what(' + clf.p%('"%s"'%shortDiscrib(tostr, 20)) + clf.b%')'+'-'*15)
    dira(anything, deep=2, __printClassFathers=False)
    print()
    print((colorFormat.b%'Document: \n'+'└── '+tabstr(doc, 5)+'\n'))    

    innerStruct = isinstance(anything, (list,tuple,dict)) or (typestr(anything) in StructLogFuns)
    if innerStruct:
        print((colorFormat.b%'Inner Struct:'))
        tree(anything, maxprint=not(full) and 12)
        print()
        
    print((colorFormat.b%'Classes: \n'+'└── '+classes+'\n'))    
    print((colorFormat.b%'To Str: \n'+'└── "'+tabstr(tostr, 5)+'"\n'))

what = FunAddMagicMethod(what)
wtf = what

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
    print('Dims:')
    for dim in dims:
        print('\t %s dim: %d'%(dim,lens.count(dim)))
    if len(dims)!=1:
        maxx = max(dims)
        arr=[s+(-1,)*(maxx-len(s)) for s in shapes]
    arr=np.array(arr)
    maxx, minn = [],[]
    for dim in range(max(dims)):
        a = arr[:,dim]
        maxx.append(a[a!=-1].max())
        minn.append(a[a!=-1].min())
    
    print('Shape:\n \t max shape: %s\n \t min shape: %s'%(maxx,minn))
    if returnn:
        return shapes

__color10 = [
 (1.0, 1.0, 1.0),
 (0.8666666666666667, 1.0, 1.0),
 (0.8, 1.0, 1.0),
 (0.6666666666666667, 1.0, 1.0),
 (0.5333333333333333, 1.0, 1.0),
 (0.4666666666666667, 1.0, 1.0),
 (0.33333333333333337, 1.0, 1.0),
 (0.19999999999999996, 1.0, 1.0),
 (0.1333333333333333, 1.0, 1.0),
 (0.06666666666666665, 1.0, 1.0)]

def getHsvColors(hn,sn,vn):
    '''
    在hsv空间产生尽可能不同的颜色集
    hn,sn,vn 分别表示 h，s，v对应每个通道的可选值的数目
    return `hn*sn*vn`个 以float三元组为HSV颜色形式的list
    '''
    def toNcolor(n,incloud0=False):
        if incloud0:
            n -= 1
        l = [1.-i*1./n for i in range(n)]
        if incloud0:
            return l+[0.]
        return l
    
    hs,ss,vs = list(map(toNcolor,[hn,sn,vn]))
    cs = []
    for s in ss:
        for v in vs:
            for h in hs:
                c = (h,s,v)
                cs += [c]
    return cs

def getDefaultColorList(colorNum=None, includeBackGround=None,uint8=False):
    '''
    产生尽可能不同的颜色集，用于多label上色
    
    Parameters
    ----------
    colorNum : int, default None
        颜色数目,default 21
    includeBackGround : bool or int, default None
        None: 没有背景色 即不包含黑色
        1 : 第一类为背景即黑色 
        -1: 最后一类为背景即黑色
    uint8 : bool, default False
        是否返还 np.uint8 格式的颜色
        
    Return
    ----------
    以float三元组为RGB颜色形式的list
    '''
    if colorNum is None:
        colorNum=21
        includeBackGround=1
    if includeBackGround is not None:
        colorNum -= 1
    
    if colorNum <= 12:
        colors = getHsvColors(6, 1, 2)
        
    elif colorNum <= 20:
        colors = __color10+[(c[0],1.0,.5) for c in __color10]
    elif colorNum <= 30:
        colors = __color10+[(c[0],1.0,.66666) for c in __color10]+[(c[0],1.0,.333333) for c in __color10]
        
    elif colorNum <= 60:
        colors = getHsvColors(colorNum//3+1 if colorNum%3 else colorNum//3,1,3)
    else :
        colors = getHsvColors(colorNum//6+1,2,3)
    
    if includeBackGround == -1:
        colors = colors[:colorNum] + [(0.,0.,0.)]
    elif includeBackGround is not None:
        colors = [(0.,0.,0.)] + colors[:colorNum]
    else:
        colors = colors[:colorNum] 
    if uint8 :
        return list((np.array(colors)*255).astype(np.uint8))
    
    from colorsys import hsv_to_rgb
    toRgb = lambda hsv:hsv_to_rgb(*hsv)
    return list(map(toRgb,colors))

def labelToColor(label, colors=None, includeBackGround=None):
    '''
    将颜色集colors映射到label上 返回彩色的label图

    Parameters
    ----------
    label : W*H of int
        W*H的labelMap
    colors : list of RGB color, default None
        对应k类的RGB颜色集，若为None 则会自动生成尽可能不同的颜色集
    includeBackGround : bool or int, default None
        若colors为None 情况下才生效:
            None: 生成的颜色集没有背景色 即不包含黑色
            1   : 第一类为背景即黑色 
            -1  : 最后一类为背景即黑色
    '''
    if colors is None:
        colors = getDefaultColorList(label.max()+1, includeBackGround=includeBackGround)
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
    from ..ylnp import isNumpyType
    if img.ndim == 2:
        img = greyToRgb(img)
    if img.dtype == np.uint8:
        img = img/255.
    if isNumpyType(img, bool):
        img = img*1.0
    if isNumpyType(img, float):
        return img
    
def getMeanStd(imgPaths):
    '''
    map reduce的方式 获取 所有uint8图片的 mean 和 std
    '''
    paths = imgPaths
    reduceDim = lambda img,axis=0:reduce(lambda x,y:np.append(x,y,axis),img)
    logg = LogLoopTime(paths)
    n = 0
    squre = np.float128([0,0,0])
    summ = np.float128([0,0,0])
    for p in paths:
        pixs = reduceDim(imread(p))/255.
        n += len(pixs)
        squre += (pixs**2).sum(0)
        summ += pixs.sum(0)
        logg(p)
    mean = summ/float(n)
    var = (squre/float(n) - mean**2)
    std = var**.5
    return mean, std

    
if __name__ == '__main__':

    pass
