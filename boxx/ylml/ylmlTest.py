# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import numpy as np
import pandas as pd

from ..tool import dynamicWraps, findints, glob,dicto
from ..ylnp import isNumpyType
from ..ylimg import (mapp, labelToColor)

from ylmlEvalu import Evalu

def binaryDiff(re,gt,size=0.5,lines=50,bound=False):
    '''
    对二分类问题的结果上色
    False Positive: red mgrid
    False Negative: blue mgrid
    lines: 网格线条的间距
    size:线条多粗 即线条是间距的多少倍
    bound:是否画出边缘
    '''
    re, gt = re > 0.5, gt > 0.5
    rem = np.zeros(gt.shape,int)
    tp = (re) * (gt)
#    tn = (~re) * (~gt)
    fp = re*(~gt)
    fn = (~re)*gt
#    show(tp,tn,fp,fn)
    rem[tp] = 1
    rem[fp] = 2
    rem[fn] = 3
    c=[[0]*3,[1]*3,[1,0,0],[.1,.1,.6]]
    diff = classDiff(rem,re,c,size=size,lines=lines,bound=bound)
    return diff

def drawBoundAndBackground(img,mask,bg=None,replace=False,lines=50,
                           size=0.2,bound=True,boundmode='thick'):
    '''
    给出mask 将给mask区域填充背景色bg的线条 并加上黑白边框
    mask: 所要标注区域
    bg : 背景填充 可以为颜色|图片 默认为红色
    replace : 是否在原图上操作
    lines: 线条的间距
    size:线条多粗 即线条是间距的多少倍
    bound:是否画出边缘
    boundmode: thick 粗正好在边界 'inner'只在前景里面 但是较细
    '''
    assert mask.ndim ==2, u'mask 必须为布尔值'
    if not mask.any():
        return img
    isint = isNumpyType(img,int)
    if not replace:
        img = img.copy()
    if bg is None:
        bg =  [max(255,img.max()),128,0]if isint else [1.,.5,0]
    white = max(255,img.max()) if isint else 1.
    m,n=img.shape[:2]
    i,j = np.mgrid[:m,:n]
    
    step = (m+n)//2//lines
    a = int(step*(1-size))
    drawInd = ~np.where(((i%step<a)& (j%step<a)),True,False)
#    from tool import g
#    g.x = mask,drawInd, bg,img
    if isinstance(bg,np.ndarray) and bg.ndim >=2:
        img[mask*drawInd] = bg[mask*drawInd]
    else:
        img[mask*drawInd] = bg
    if bound:
        from skimage.segmentation import find_boundaries
        boundind = find_boundaries(mask, mode=boundmode,background=True)
        boundBg = np.where((i+j)%10<5,white,0)
        img[boundind] = boundBg[boundind][...,None]
    return (img)
   
def classDiff(rem,gtm,colors=None,size=.15,reMod=False,lines=50,bound=True):
    '''
    对多分类问题的gt进行上色
    对于错误分类 加网格(网格颜色是resoult的颜色) 加有边框
    rem :多分类结果 二维矩阵
    gtm :GroundTruth
    colors:标签对应的颜色
    size:网格所占用的比重
    reMod:对resoult上色, 对于错误分类 网格颜色是 GroundTruth的颜色
    lines:网格线的数量
    bound:是否画出边缘
    '''
    assert rem.ndim==2 and gtm.ndim==2,"rem,gtm 's dim must be 2"
    rgb = labelToColor(rem if reMod else gtm, colors) 
    clas = range(len(colors))
    for c,color in enumerate((colors)): #c mean iter every Class
        for oc in clas: # oc means OtherClass
            if oc==c:
                continue
            mask = (rem==c)*(gtm==oc)
            if mask.any():
                bg = colors[oc if reMod else c]
#                print bg,c,oc
                drawBoundAndBackground(rgb,mask,bg,bound=bound,
                                       size=size,replace=True,lines=lines)
    return rgb

def confusionMatrix(re,gt,classn=None):
    '''求混淆矩阵（confusion matrix）
    
    Parameters
    ----------
    re : np.ndarray
        resoult , 预测的标签
    gt : np.ndarray 
        ground Truth, 值为每个像素的类别
    classn : int,  default None
        总类别数目 默认为 max(re.max(), gt.max())
    '''
    if classn is None:
        classn = max(re.max(), gt.max())
    ma = np.zeros((classn,classn),int)
    for ind in range(classn):
        row = np.histogram(re[(gt==ind)],classn,range=(0,classn))[0]
        ma[ind][:] = row[:]
    return ma



def f1Score(re,gt,classn):
    '''求各个类别的f1Score 
    先求混淆矩阵（confusion matrix）
    
    Parameters
    ----------
    re : np.ndarray
        resoult or prob, 预测的标签或h*w*n 的概率矩阵
    gt : np.ndarray 
        ground Truth, 值为每个像素的类别
    classn : int
        总类别数目
    '''
    if re.ndim == 3:
        re = re.argmax(2)
    cma = confusionMatrix(re,gt,classn)
    ma = np.float64(cma)
    tp = ma[range(classn),range(classn)]
    fp = ma.sum(0)-tp
    fn = ma.sum(1)-tp
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = 2*precision*recall/(precision+recall)
    return f1

@dynamicWraps
def getWeightCore(hh,ww=None,mappFun=None,seta=0.5):
    '''
    返回一个权重二维矩阵 ，默认是seta=0.5的二维高斯分布
    mappFun: 对矩阵每个点执行mappFun(i,j) 返回的结果构成二维矩阵
    '''
    if ww is None:
        ww = hh
    if mappFun is None:
#        ijToCenter = lambda x,i,j:(((i/float(hh)-1/2.)**2+(j/float(ww)-1/2.)**2))
#        wc = weightCore = mapp(ijToCenter,weightCore,need_i_j=True)
        i,j = np.mgrid[:hh,:ww]
        wc = (((i/float(hh)-1/2.)**2+(j/float(ww)-1/2.)**2))
        wc = 1./(2*np.pi*seta**2)*np.e**(-wc/(2*seta**2))
        wc = wc/wc.max()
        #show(normalizing(img[:hh,:ww]*wc[...,None]),img[:hh,:ww])
#        polt3dSurface(wc)
        return wc
    weightCore = np.zeros((hh,ww))
    return mapp(lambda x,i,j:mappFun(i,j),weightCore,need_i_j=True)

def smallImg(img,simgShape, step=None,f=None):
    '''
    将大图切割成固定大小的小图,使产生的小图能覆盖大图的所有面积

    Parameters
    ----------
    simgShape : int or tuple or float
        小图片的shape,为int时候 自动转换为(simgShape, simgShape)
        为float时候 转换为 (int(h*simgShape),int(w*simgShape))
    step : float or int or tuple(steph,stepw),defalut None
        h和w方向上 相邻切割的步长, 默认为simgShape 
        float : (int(step*simgShape[0]),int(step*simgShape[1]))
        int : (step, step)
    fun : funcatin, default None
        若有fun 则执行fun(simg,i,j)
        其中：
            simg:被切割的小图片
            i: simg所在img的row
            j: simg所在img的col
    
    Returns
    -------
    simgs : list of ndarray
        切割出来的小图的list
    '''
    h,w = img.shape[:2]
    if isinstance(simgShape,float):
        hh,ww = (int(h*simgShape),int(w*simgShape))
    if isinstance(simgShape,int):
        hh,ww = simgShape,simgShape
    if isinstance(simgShape,(tuple,list)):
        hh,ww = simgShape
    if step is None:
        steph,stepw = hh,ww
    if isinstance(step,int):
        steph,stepw = step,step
    if isinstance(step,float):
        steph,stepw = int(hh*step),int(ww*step)
    if isinstance(step,(tuple,list)):
        steph,stepw = step
    simgs = []
    for i in range(0,h-hh,steph)[:]+[h-hh]:
        for j in range(0,w-ww,stepw)[:]+[w-ww]:
            simg = img[i:i+hh,j:j+ww]
            simgs.append(simg)
            if f:
                f(simg,i,j)
    return simgs


def autoSegmentWholeImg(img,simgShape,handleSimg,step=None,weightCore=None):
    '''
    将img分割到 shape为simgShape 的小图simg，执行handleSimg(simg)
    将所有handleSimg(simg)的结果自动拼接成img形状的ndarray并返回
    
    Parameters
    ----------
    img : ndarray
        需要被分割处理的图片
    simgShape : int or tuple
        小图片的shape,为int时候 自动转换为(simgShape, simgShape)
    handleSimg : funcation
        用于处理shape为simgShape的小图片的函数 
        此函数需要接受一个ndarray作为参数并返回shape[:2]同为为(h,w)的ndarray
        即：handleSimg(simg)=>ndarray，比如 net.pridict(simg)
    step : float or int or tuple(steph,stepw),defalut None
        h和w方向上 相邻切割的步长, 默认为simgShape 
        float : (int(step*simgShape[0]),int(step*simgShape[1]))
        int : (step, step)
    weightCore : {None,'avg','gauss',ndarray}, defalut None 
        对于两个simg图片重叠部分进行融合时候的各自权重
        默认取距离simg中心最近的部分
       'gauss':在重叠部分 采用高斯分布 使之离simg中心越远，权重越低
       'avg':重叠部分取平均
    
    Returns
    -------
    result : ndarray
        shape[:2]等于img.shape[:2]的ndarray
    '''
    if isinstance(simgShape,int):
        hh,ww = simgShape,simgShape
    hh,ww = simgShape
    h,w = img.shape[:2]
    if weightCore is None:
        pass
    elif isinstance(weightCore,np.ndarray):
        pass
    elif weightCore in ['avg']:
        weightCore = np.ones((hh,ww))
    elif weightCore in ['guss','gauss']:
        weightCore = getWeightCore(hh,ww)
    else:
        raise Exception,'Illegal argus `weightCore` in `autoSegmentWholeImg`!'
    weight = np.zeros((h,w))
    class c:
        re=None
        near=None
    def f(simg,i,j):
        sre = handleSimg(simg)
        if c.re is None:
            c.re = np.zeros((h,w)+sre.shape[2:],sre.dtype)
        if weightCore is None:
            if c.near is None:
                y,x = np.mgrid[:hh,:ww]
                c.near = 1-((x*1./ww-1./2)**2+(y*1./hh-1./2)**2)**.5
            ind = c.near > weight[i:i+hh,j:j+ww]
            c.re[i:i+hh,j:j+ww][ind]= sre[ind]
            weight[i:i+hh,j:j+ww][ind]= c.near[ind]
            return
        oldw = weight[i:i+hh,j:j+ww]
        ws = weightCore
        if sre.ndim!=2:
            ws = ws[...,None]
            oldw = oldw[...,None]
    #    map(loga,[ws,sre,c.re,oldw,c.re[i:i+hh,j:j+ww]*oldw])
        c.re[i:i+hh,j:j+ww] = (ws*sre + c.re[i:i+hh,j:j+ww]*oldw)/(ws+oldw)
        weight[i:i+hh,j:j+ww] += weightCore
    #    show(c.re,weight)
    (smallImg(img,(hh,ww),step=step,f=f))
    return c.re

class ArgList(list):
    '''
    标记类 用于标记需要被autoFindBestParams函数迭代的参数列表
    '''
    pass

    
def autoFindBestParams(c, args,evaluFun,sortkey=None, savefig=False):
    '''遍历args里面 ArgList的所有参数组合 并通过sortkey 找出最佳参数组合
    
    Parameters
    ----------
    c : dicto
        即configManager 生成的测试集的所有环境配置 c
        包含args，数据配置，各类函数等
    args : dicto
        predict的参数，但需要包含 ArgList 类 将遍历ArgList的所有参数组合 并找出最佳参数组合
    evaluFun : Funcation
        用于评测的函数，用于Evalu类 需要返回dict对象
    sortkey : str, default None
        用于筛选时候的key 默认为df.columns[-1]
    
    Return: DataFrame
        每个参数组合及其评价的平均值
    '''
    iters = filter(lambda it:isinstance(it[1],ArgList),args.items())
    iters = sorted(iters,key=lambda x:len(x[1]),reverse=True)
    argsraw = args.copy()
    argsl = []
    args = dicto()
    
    k,vs = iters[0]
    lenn = len(iters)
    deep = 0
    tags = [0,]*lenn
    while deep>=0:
        vs = iters[deep][1]
        ind = tags[deep]
        if ind != len(vs):
            v = vs[ind]
            tags[deep]+=1
            key = iters[deep][0]
            args[key] = v
            if deep == lenn-1:
                argsl.append(args.copy())
            else:
                deep+=1
        else:
            tags[deep:]=[0]*(lenn-deep)
            deep -= 1
    assert len(argsl),"args don't have ArgList Values!!"
    pds,pddf = pd.Series, pd.DataFrame
    edic={}
    for arg in argsl:
        argsraw.update(arg)
        c.args.update(argsraw)
        e = Evalu(evaluFun,
                  evaluName='tmp',
                  sortkey=sortkey,
                  loged=False,
                  saveResoult=False,
                  )
        if 'reload' in c:
            reload(c.reload)
            inference = c.reload.inference
        elif 'predictInterface' in c:
            reload(c.predictInterface)
            inference = c.predictInterface.predict
        else:
            raise Exception,  "don't reload get c.reload"
        for name in c.names[::]:
            gt = c.readgt(name)
            prob = inference(c.toimg(name))
            re = prob.argmax(2)
#            from boxx import g
#            g.re,g.gt = re,gt
            e.evalu(re,gt,name)
    #        img = readimg(name)
    #        show(re,gt)
    #        show(img)
        if sortkey is None:
            sortkey = e.columns[-1]
        keys = tuple(arg.values())
        for k,v in arg.items():
            e[k] = v
        edic[keys] = e
        print 'arg: %s\n'%str(arg), e.mean()
    es = pddf(map(lambda x:pds(x.mean()), edic.values()))
    print '-'*20+'\nmax %s:\n'%sortkey,es.loc[es[sortkey].argmax()]
    print '\nmin %s:\n'%sortkey,es.loc[es[sortkey].argmin()]
    if len(iters) == 1:
        k = iters[0][0]
        import matplotlib.pyplot as plt
        df = es.copy()
        df = df.sort_values(k)
        plt.plot(df[k],df[sortkey],'--');plt.plot(df[k],df[sortkey],'rx')
        plt.xlabel(k);plt.ylabel(sortkey);plt.grid()
        if savefig:
            plt.savefig(savefig)
            plt.close()
        else:
            plt.show()    
    return es

def autoFindBestEpoch(c, evaluFun,sortkey=None,epochs=None, savefig=False):
    '''遍历所有epoch的weight  并通过测试集评估项sortkey 找出最佳epoch
    
    Parameters
    ----------
    c : dicto
        即configManager 生成的测试集的所有环境配置 c
        包含args，数据配置，各类函数等
    evaluFun : Funcation
        用于评测的函数，用于Evalu类 需要返回dict对象
    sortkey : str, default None
        用于筛选时候的key 默认为df.columns[-1]
    
    Return: DataFrame
        每个参数组合及其评价的平均值
    '''
    args = c.args
    if not isinstance(epochs,(tuple,list)) :
        pas = [p[len(args.prefix):] for p in glob(args.prefix+'*') if p[-4:]!='json']
        eps = map(lambda s:len(findints(s)) and findints(s)[-1],pas)
        maxx = len(eps) and max(eps)
        minn = len(eps) and min(eps)
        if isinstance(epochs,int):
            epochs = range(minn,maxx)[::epochs]+[maxx]
        else:
            epochs = range(minn,maxx+1)
    args['restore'] = ArgList(epochs)
#    print epochs
    df = autoFindBestParams(c, args, evaluFun,sortkey=sortkey,savefig=savefig)
    return df

if __name__ == '__main__':
    pass
