# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import numpy as np
from ylimg import imread


from collections import Iterator 
class GenSimg(Iterator):
    '''
    随机生成小图片simg及gt 的迭代器，默认使用1Gb内存作为图片缓存
    默认生成simg总面积≈所有图像总面积时 即结束
    '''
    def __init__(self, imggts, simgShape, handleImgGt=None,
                 batch=1, cache=None,iters=None,
                 timesPerRead=1,infinity=False):
        '''
        imggts: zip(jpgs,pngs)
        simgShape: simg的shape
        handleImgGt: 对输出结果运行handleImgGt(img,gt)处理后再返回
        batch: 每次返回的batch个数
        cache: 缓存图片数目, 默认缓存1Gb的数目
        timesPerRead: 平均每次读的图片使用多少次(不会影响总迭代次数),默认1次
        iters: 固定输出小图片的总数目，与batch无关
        infinity: 无限迭代
        '''
        if isinstance(simgShape,int):
            simgShape = (simgShape,simgShape)
        self.handleImgGt = handleImgGt
        self.imggts = imggts
        self.simgShape = simgShape
        self.batch = batch
        self._iters = iters
        self.iters = self._iters
        self.infinity = infinity
        
        hh,ww = simgShape
        jpg,png = imggts[0]
        img = imread(jpg)
        h,w = img.shape[:2]
        if cache is None:
            cache = max(1,int(1e9/img.nbytes))
        cache = min(cache,len(imggts))
        self.maxPerCache = int(cache*(h*w)*1./(hh*ww))* timesPerRead/batch
        self.cache = cache
        self.n = len(imggts)
        self._times = max(1,int(round(self.n*1./cache/timesPerRead)))
        self.times = self._times
        self.totaln = self.sn = iters or int((h*w)*self.n*1./(hh*ww))
        self.willn = iters or self.maxPerCache*self.times*batch
        self.count = 0
        self.reset()
        
        self.bytes = img.nbytes
        argsStr = '''imggts=%s pics in dir: %s, 
        simgShape=%s, 
        handleImgGt=%s,
        batch=%s, cache=%s,iters=%s,
        timesPerRead=%s, infinity=%s'''%(self.n , os.path.dirname(jpg) or './', simgShape, handleImgGt,
                                 batch, cache,iters,
                                 timesPerRead,infinity)
        generatorStr = '''maxPerCache=%s, readTimes=%s
        Will generator maxPerCache*readTimes*batch=%s'''%(self.maxPerCache, self.times,
                                                          self.willn)
        if iters:
            generatorStr = 'Will generator iters=%s'%iters
        self.__describe = '''GenSimg(%s)
        
        Total imgs Could generator %s simgs,
        %s simgs.
        '''%(argsStr,self.totaln,
             generatorStr,)
    def reset(self):
        if (self.times<=0 and self.iters is None) and not self.infinity:
            self.times = self._times
            raise StopIteration
        self.now = self.maxPerCache
        inds = np.random.choice(range(len(self.imggts)),self.cache,replace=False)
        datas = {}
        for ind in inds:
            jpg,png = self.imggts[ind]
            img,gt = imread(jpg),imread(png)
            datas[jpg] = img,gt
        self.data = self.datas = datas
        self.times -= 1
    def next(self):
        self.count += 1
        if (self.iters is not None) and not self.infinity:
            if self.iters <= 0:
                self.iters = self._iters
                raise StopIteration
            self.iters -= self.batch
        if self.now <= 0:
            self.reset()
        self.now -= 1
        hh,ww = self.simgShape
        datas = self.datas
        imgs, gts = [], []
        for t in range(self.batch):
            img,gt = datas[np.random.choice(datas.keys(),1,replace=False)[0]]
            h,w = img.shape[:2]
            i= np.random.randint(h-hh+1)
            j= np.random.randint(w-ww+1)
            (img,gt) =  img[i:i+hh,j:j+ww],gt[i:i+hh,j:j+ww]
            imgs.append(img), gts.append(gt)
        (imgs,gts) = map(np.array,(imgs,gts))
        if self.handleImgGt:
            return self.handleImgGt(imgs,gts)
        return (imgs,gts)
    @property
    def imgs(self):
        return [img for img,gt in self.datas.values()]
    @property
    def gts(self):
        return [gt for img,gt in self.datas.values()]
    def __str__(self):
        batch = self.batch
        n = len(self.datas)
        return self.__describe + \
        '''
    status:
        iter  in %s/%s(%.2f)
        batch in %s/%s(%.2f)
        cache imgs: %s
        cache size: %.2f MB
        '''%(self.count*batch,self.willn,self.count*1.*batch/self.willn,
            self.count,self._times*self.maxPerCache,
            self.count*1./(self._times*self.maxPerCache),
            n, (n*self.bytes/2**20))
        
    __repr__ = __str__

if __name__ == '__main__':
    pass
