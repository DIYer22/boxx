# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from ..ylcompat import interactivePlot
from ..tool.toolLog import LogLoopTime,log
from ..tool import pathjoin, getFunName
from ..ylnp import savenp, loadnp
import pandas as pd
import numpy as np


def accEvalu(re, gt):
    '''评估二分类分割问题 返回dict 包含 acc 和 loss
    
    Parameters
    ----------
    re : np.ndarray
        resoult or prob, 标签或h*w*n 的概率矩阵
    gt : np.ndarray of bool
        ground Truth, 值为每个像素的类别
    '''
    if re.ndim == 3:
        re = re.argmax(2)
    acc = (re==gt).sum()/float(gt.shape[0]*gt.shape[1])*100
    return {'acc':acc,'loss':100-acc}
    

def lplrEvalu(re, gt):
    '''评估二分类分割问题 返回dict 包含 ['LP', 'LR', 'OP', 'OR','me']'''
    re = re > 0
    TPl = (re==0)*(gt==0) #(re+gt) == 0
    FPl = (re==0)*(gt==1)
    FNl = (re==1)*(gt==0)
    

    TPs = (re==1)*(gt==1) 
    FPs = (re==1)*(gt==0)
    FNs = (re==0)*(gt==1)
#    show([TPs,FPs,FNs])
    TPl,FPl,FNl,TPs,FPs,FNs = [float(i.sum()) for i in [TPl,FPl,FNl,TPs,FPs,FNs]]
    LP = TPl/(TPl+FPl)
    LR = TPl/(TPl+FNl)
    OP = (TPl+TPs)/(TPl+FPl+TPs+FPs)
    OR = (TPl+TPs)/(TPl+FNl+TPs+FNs)
#    return (LP*100,LR*100,OP*100,OR*100)
    mean = np.mean([LP,LR,OP,OR])
    return {k:100*(1-v) for k,v in zip(['LP', 'LR', 'OP', 'OR','me'],[LP,LR,OP,OR,mean])}

def diceEvalu(re,gt):
    ''' Dice coefficient 方法评估二分类分割问题 返回dict 包含 ['dice', 'loss']
    
    Parameters
    ----------
    re : np.ndarray
        resoult or prob, 标签或h*w*n 的概率矩阵
    gt : np.ndarray of bool
        ground Truth, 值为每个像素的类别
        '''
    if re.ndim == 3:
        re = re.argmax(2)
    dice = (re*gt).sum()*2/float(re.sum()+gt.sum())*100
    return {'dice':dice,'loss':100-dice,}



class Evalu(pd.DataFrame):
    '''
# 用于验证的工具类Evalu
继承自pandas.DataFrame， 会自动保存每个样本 resoult 及其评估结果，能对评估结果进行分析
并能以DataFrame的形似对评估结果操作与分析
常用缩写：
    * evalu = Evalu的实例
    * re = resoult, 需要评测的样本 
    * gt = GroundTruth, 用于评测的真值 
    * key = 评测项的名称 即列的名称 属于 self.columns
    * df = pd.DataFrame 实例
    * prob = 分割的概率矩阵 ，即shape为 h*w*n 的矩阵(n 表示类别数)
    
功能
--------
自动log :
    对每个样本 自动log出当前进度，当前迭代花费的时间，及评估结果
保存resoult :
    将用来评估的resoult保存为压缩的npz格式
    通过 evalu.re(name) 或者evalu[name] 来调用
载入之前的评估结果 :
    将loadcsv=True 或者 对应评估结果csv的路径即可载入
分析与可视化 :
    总结 :evalu.summary()
    可视化评估项的分布 :evalu.distr(key)
一键删除验证产生的所有文件 :
    evalu.removeFiles()
继承 pandas.DataFrame 的所有操作 :
    以df形似 分析evalu后的结果 
    ps:pandas快速入门 http://wiki.jikexueyuan.com/project/start-learning-python/311.html

Examples
--------
>>> names = glob("/home/[to val path]/*.jpg")
e = Evalu(binaryEvalu,
          evaluName='try-example',
          valNames=names,
          logFormat='acc:{acc:.4f}, loss:{loss:.4f}',
          sortkey='acc'
          )
for name in names:
    [get re,gt code]
    e.evalu(re,gt,name)
e.summary()
e.distr()
    '''
    def __init__(self,evaluFun,
                 evaluName='null',
                 valNames=None,
                 logFormat=None,
                 sortkey=None,
                 loadcsv=False,
                 saveResoult = False,
                 loged=True,
                 savepath='./val/',
                 ):
        '''
Parameters
----------
evaluFun : funcation
    用于评估resoult的函数，此函数须接受两个参数 (re,gt),并返回一个dict
    dict 包含每一个评估项的值
    例如 evaluFun(re,gt) => return {'key1':value1,'key2':value2}
evaluName : str, default 'null'
    实例的名称
valNames : list or tuple, default None
    验证集所有样本的名字
logFormat : str, default None
    fromat格式 用于规范评估结果的显示效果  
    会执行 print logFormat.format(**evaluFun(re,gt))
    如: 'key1 is {key1:.2f}, key2 is {key2:.2f},'
    默认为直接打印 evaluFun(re,gt)
sortkey : str, default None
    用于排序时候的key 默认为df.columns[-1]
loadcsv : bool or str, default False
    载入已保存的csv 默认不载入，为True时候则载入，
    为str时候则载入str对应的path的csv
saveResoult : bool or funcation, default False
    是否保存resoult 默认为False ,True  则保存 re
    若为funcation 则保存 saveResoult(re) 为 .npz格式
loged : bool, default True
    是否每次评估都打印出结果 默认为打印
savepath : str, default './val/'
    保存的路径 若loadcsv 为path 则为 dirname(loadcsv)

Examples
--------
e = Evalu(accEvalu,
          evaluName='binary segment evalu',
          valNames=names,
          logFormat='acc:{acc:.4f}, loss:{loss:.4f}',
          sortkey='loss'
          )
        '''
        pd.DataFrame.__init__(self,)
        self._inited = False
        self.evaluName = evaluName
        self.evaluFun = evaluFun
        self.logFormat = logFormat
        self.logLoop = LogLoopTime(valNames,loged=False)
        self.n = -1 if valNames is None else len(valNames)
        self.sortkey = sortkey
        self.loged = loged
        self.saveResoult = saveResoult
        self.__isTuple = False
        
        if isinstance(loadcsv,str):
            self.evaluDir = os.path.dirname(loadcsv)
        else:
            self.evaluDir = os.path.join(savepath,'Evalu-%s'%evaluName)
        self._defaultCsvPath = pathjoin(self.evaluDir,self.evaluName+'.csv')
        if loadcsv :
            if isinstance(loadcsv,str):
                self._defaultCsvPath = loadcsv 
            self._loaddf()
    def _initdf(self,name,dic):
        self._inited = True
        dic['name'] = name
        pd.DataFrame.__init__(self,[pd.Series(dic)])
        self.set_index('name',inplace=True)
        if self.sortkey is None:
            self.sortkey = self.columns[-1]
    def _loaddf(self):
        self._inited = True
        pd.DataFrame.__init__(self,pd.read_csv(self._defaultCsvPath,index_col='name'))
        if self.sortkey is None:
            self.sortkey = self.columns[-1]
        
    def __makedirs(self):
        path = pathjoin(self.evaluDir,'npzs')
        if not os.path.isdir(path):
            os.makedirs(path)
    def _log(self,s):
        if self.loged:
            log('%s'%s)
    def evalu(self, re, gt, name=None):
        '''使用 self.evaluFun 评估 resoult GrountdTruth
        
        Parameters
        ----------
        re : as parameters of self.evaluFun
            需要评测的resoult
        gt : as parameters of self.evaluFun
            用于评测的真值 GroundTruth
        name : str, default None
            记录此次评估样本的名称 为空则不记录    
        '''
        dic = self.evaluFun(re,gt)
        s = self._formatDic(dic)
        if name is None:
            self._log(s)
            return dic
        if not self._inited:
            self._initdf(name,dic)
        else:
            self.loc[name] = dic
        if self.logLoop:
            loopLog = self.logLoop(name)
            s = (loopLog+' Evalu:'+s)
        self._log(s)
        if len(self)==self.n and self.index[-1] == name and (
                self.loged or self.saveResoult):
            self.savecsv()
        if self.saveResoult:
            self._savere(name,re)
        return dic
    def savecsv(self,):
        self.__makedirs()
        self.to_csv(self._defaultCsvPath)
    def _savere(self,name,re):
        self.__makedirs()
        npname = pathjoin(self.evaluDir,'npzs',name)
        if '__call__' in dir(self.saveResoult) :
            savenp(npname,self.saveResoult(re))
        else:
            if re.ndim == 3:
                re = np.uint8(re.argmax(2))
            savenp(npname,re)
    def re(self,name=-1):
        '''return np.array, 返回自动保存下来的np.array 样本
        
        Parameters
        ----------
        name : str or int, default -1
            当为int 时 name=df.index[int]    
        '''
        if isinstance(name,int):
            name = self.index[name]
        npname = pathjoin(self.evaluDir,'npzs',name)
        re = loadnp(npname)
        return re
    def __getitem__(self,name):
        '''同 Evalu.re
        return np.array, 返回自动保存下来的np.array 样本
        
        Parameters
        ----------
        name : str or int, default -1
            当为int 时 name=self.index[int]  
        '''
        if name in self.columns:
            return pd.DataFrame.__getitem__(self,name)
        return  self.re(name)
    
    def _sorted(self,key,ascending=True):
        if isinstance(key,int) and key not in self.columns:
            key = self.columns[key]
        if key is None:
            key = self.sortkey
        return self.sort_values(key,ascending=ascending)
    @property
    def highh(self):
        return self.high()
    def high(self,n=10,key=None):
        '''return df, 评估项key 最高的n个样本组成的df
        
        Parameters
        ----------
        n : int, default 10
            返回的样本数目   
        key: key in self.columns, default self.sortkey
            用于计算排名的 key
        '''
        df = self._sorted(key,ascending=False)
        return df.head(n)
    @property
    def loww(self):
        return self.low()
    def low(self,n=10,key=None):
        '''与evalu.high 相反 参见evalu.high
        '''
        df = self._sorted(key)
        return df.head(n)
    @interactivePlot
    def distr(self, key=None):
        '''分析key 的分布，describe + 分布图
        
        Parameters
        ----------
        key : str or int, default self.sortkey
            当为int 时 key=df.columns[int]
        '''
        import matplotlib.pyplot as plt
        if isinstance(key,int) and key not in self.columns:
            key = self.columns[key]
        key = self.sortkey if key is None else key 
        df = self._sorted(key,False)
        print((df[key].describe()))
        df['_index_'] = list(range(1,len(df)+1)) 
        df['__mean'] = mean = df[key].mean()
        df.set_index('_index_',inplace=True)
        df['__mean'].plot(style='orange')
        df[key].plot.bar(title='mean = %s'%mean)
        plt.show()
    
    def _formatDic(self,dic):
        formatt = self.logFormat
        if formatt:
            s=(formatt.format(**dic))
        else:
            s=(', '.join(['%s: %s'%(k,v) for k,v in list(dic.items())]))
        return s
    def __topAndLowStr(self,n=10):
        top = self.high(n)
        low = self.low(n)
        tops = str(top[self.sortkey]).split('\n')
        title , tops = tops[-1], tops[1:-1]
        lows = str(low[self.sortkey]).split('\n')[1:-1]
        strn = len(lows[0])+1
        second = ('high %d'%n+strn*' ')[:strn]+'| '+('low %d'%n)
        body='\n'.join([t+' | '+l for t,l in zip(tops,lows)])
        s= '''evaluName: %s, sortkey%s
%s
%s
'''%(self.evaluName, title[4:], second, body)
        return (s)
    def __str__(self,n=3):
        funName = getFunName(self.evaluFun)
        describe = self.describe()
        s = '''Evalu name       : %s
cache resoult dir: %s
sort key         : %s
evalu funcation  : %s
logFormat        : %s
        ''' %(self.evaluName,self.evaluDir,self.sortkey,funName,self.logFormat)
        
        return s+'\n'+self.__topAndLowStr(n)+str(describe)
    __repr__ = pd.DataFrame.__str__
    def summary(self,n=10):
        '''various summary 
        n:同时显示high和low的数量'''
        print(self.__str__(n))
        
    class Series(pd.Series):
        '''改造了 __str__ 的 pd.Series'''
        def __init__(self,series,strr):
            pd.Series.__init__(self,series)
            self.strr = strr
        def __str__(self):
            return self.strr
        __repr__ = __str__
    def __call__(self,name=-1,sortkey=None):
        '''return pd.Series, 对应name的评估结果
        
        Parameters
        ----------
        name : str or int, default -1
            当为int 时 name=df.index[int]    
        sortkey: key in self.columns, default self.sortkey
            用于计算排名的 key
        '''
        if isinstance(name,int):
            name = self.index[name]
        key = sortkey or self.sortkey
        row = self.loc[name]
        small,n = (self[key]<=row[key]).sum(),float(len(self))
#        row['high_in_[%s]'%key] = '%d/%d (%.2f%%)'%(small,n,small/n*100)
        dic = dict(row)
        s = "Name: %s  High in ['%s']:"%(name,key) + '%d/%d(%.2f%%)  Evalu:'%(small,n,small/n*100)
        s += self._formatDic(dic)
        return Evalu.Series(row,s)
    @property
    def df(self):
        return pd.DataFrame(self)
    
    def removeFiles(self):
        '''删除使用此Evalu产生的文件 即文件夹 self.evaluDir'''
        import shutil
        shutil.rmtree(self.evaluDir)
if __name__ == '__main__':
    e = Evalu(int)
    import pandas as pd
    df = pd.DataFrame({
                       0:list(range(5)),
                       1:list(range(10,15)),
                       'a':list("abcde"),
                       })
    df.set_index(0,inplace=True)


    pass
