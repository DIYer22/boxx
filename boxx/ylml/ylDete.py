# -*- coding: utf-8 -*-
"""
tools for detection and bounding box

@author: yl
"""
import numpy as np

from ..ylsci import Vector, cos, sin
from ..tool import sliceInt, dicto
from ..ylimg import toPng, padding


#inttuple = mf - inttuple
def cropMinAreaRect(img, rect, borderValue=None):
    import cv2
    # rotate img
    angle = rect[2]
    rows,cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows),borderValue=borderValue)
    
    # rotate bounding box
#    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]    
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1], 
                       pts[1][0]:pts[2][0]]
    return img_crop

    if 0 == 'test':
        # generate image
        img = np.zeros((1000, 1000), dtype=np.uint8)
        img = cv2.line(img,(400,400),(511,511),1,120)
        img = cv2.line(img,(300,300),(700,500),1,120)
        img = cv2.line(img,(0,0),(1000,100)[::-1],2,200)
        
        # find contours / rectangle
        _,contours,_ = cv2.findContours(img, 1, 1)
        
        # rect = ((middle_point), (w, h), angle)
        rect = cv2.minAreaRect(contours[0])
    #    rect = ((100.0, 499.5), (1999.0, 200.0), -90.0)
        print(rect)
        from boxx import timeit, show
        # crop
        with timeit():
            img_croped = cropMinAreaRect(img, rect)
        show(img)
        show(img_croped)
    
class Bbox():
    '''
    
    sbox:
        小方块 ,1. 减少旋转的计算量;2. 方便贴图
    urdl:
        mean up, right, down, left
    expandPara:
        face bbox to head bbox, evalue by Bbox.getExpandFun(imgBox, sbox, rate=256/286.)
    vx, vy:
        vx: w 方向的向量; vy: h 方向的向量
    ps, p0:
        ps: bbox 的四个定点, p0 左上角为 p0 顺时针依次类推
    
    '''
    def __init__(self, p0, w, h, deg=None, canvas=None, expandPara=None, **kv):
        vx, vy = Bbox.getVxVy(w, h, deg)
        pNose = p0 + vx/2 + vy/2
        if expandPara :
            unit = (w + h)/2
            delta = unit * expandPara.vRate
            if deg:
                delta = delta.rotation(deg)
            p0 = delta + pNose
            w = unit * expandPara.wRate
            h = unit * expandPara.hRate
            vx, vy = Bbox.getVxVy(w, h, deg)
        ps = np.array([p0, p0+vx, p0+vx+vy, p0+vy])
        
        urdl = u, r, d, l = min(ps[:, 1]), max(ps[:, 0]), max(ps[:, 1]), min(ps[:, 0])
        self.offsetToSbox = Vector([l, u])
        self.boxUrdl = None
        self.__dict__.update(locals())
    def __str__(self, ):
        p0, w, h, deg = self.p0, self.w, self.h, self.deg
        return "p0:{p0}, w:{w}, h:{h}, deg:{deg}".format(locals())
    __repr__ = __str__
    
    @staticmethod
    def getVxVy(w, h, deg=None):
        if deg is None:
            vx, vy = Vector([w, 0]), Vector([0, h])
        else:
            sinn, coss = sin(deg), cos(deg)
            vx = Vector([coss*w, sinn*w])
            vy = Vector([-sinn*h, coss*h])
        return vx, vy

#        def expand(d_urdl=[98, 44, 42, 44]):
#            178 * 218

#    @staticmethod
    def _getUrdlForCanvas(self):
        '''get sbox urdl in canvas
        '''
        if self.boxUrdl is None: 
            dx, dy = self.canvas.offset
            u, r, d, l = self.urdl
            self.boxUrdl = u+dy, r+dx, d+dy, l+dx
        return self.boxUrdl
    def cropSbox(self):
        u, r, d, l = self._getUrdlForCanvas()
        sboxImg = self.canvas.canvas[sliceInt[u:d, l:r]]
        sboxImgPng = toPng(sboxImg)
        return sboxImgPng
    def paste(self, rimg):
        '''
        rimg: result img'''
        rimg = toPng(rimg)
        w, h = self.r-self.l, self.d-self.u
        deg = - self.deg
        p2 = Vector((rimg).shape)[[1,0]]
        pad = max([w,h]-p2)/2
        padedImg = padding(rimg, pad)
        rect = (p2/2+pad, (w, h), deg)
        simgPng = cropMinAreaRect(padedImg, rect, borderValue=(0,0,0,0))
        simg, mask = simgPng[...,:3], simgPng[...,3]>0
        u, r, d, l = self._getUrdlForCanvas()
#        g()
#        self.canvas.canvas[sliceInt[u:d, l:r]][mask] = simg[mask]
        self.canvas.canvas[sliceInt[u:u+mask.shape[0], l:l+mask.shape[1]]][mask] = simg[mask]
        return self.canvas.canvas
    def crop(self, cropSboxFirst=False):
        if cropSboxFirst :
            img = self.cropSbox()
            p0 = self.p0 - self.offsetToSbox
        else:
            img = self.canvas.raw
            p0 = self.p0
        w, h, deg = self.w, self.h, self.deg
        l, u = p0
        vx, vy = self.vx, self.vy
        if deg is None:
            deg = 0
        
        pm = p0 + vx/2. + vy/2.
        rect = (pm, (w, h), deg)
        img_croped = cropMinAreaRect(img, rect, borderValue=(0,0,0,0))
        return (img_croped)
    @staticmethod
    def test():
        pass
    

class Canvas():
    '''
    a canvas to padding bound, draw bbox, paste new patch
    raw, img:
        原始图像
    canvas: 
        根据扩张后的bbox padding 的画布
    offset:
        canvas 和 raw 的坐标转换: v_canvas = v_raw + offset
    '''
    BboxClass = Bbox
    def __init__(self, img, bboxList, expandPara=None):
        self.raw = img
        self.bboxs = bboxs = []
        for bboxDic in bboxList:
            dic = dicto(canvas=self, expandPara=expandPara,)
            dic.update(dict(bboxDic))
            bbox = self.BboxClass( **dic)
#            g()
            bboxs.append(bbox)
        h, w = img.shape[:2]
        self.urdl = np.array([[0, w, h, 0]] + [b.urdl for b in bboxs])
        self.offset = dx, dy = -Vector(self.urdl[:, [3, 0]].min(0), )
        self.leftDown = self.urdl[:, [1,2]].max(0)
        ww, hh = (self.offset + self.leftDown).intround()
        self.canvas = np.zeros((hh, ww,) + img.shape[2:], img.dtype)
        self.canvas[sliceInt[dy:dy+h, dx:dx+w]] = img
#        self.bias = Vector([0, 0])
        self.__dict__.update(locals())
#        g()

    def getResult(self):
        dy, dx, h, w = self.dy, self.dx, self.h, self.w
        return self.canvas[sliceInt[dy:dy+h, dx:dx+w]]
    def show(self):
        from boxx import show, pblue
        canvas = self
        result = canvas.getResult()
        pblue('show canvas.getResult()')
        show-result
        pblue('show Bboxs.crop():')
        show-[b.crop() for b in canvas.bboxs]
        if canvas.bboxs and canvas.bboxs[0].deg:
            pblue('show Bboxs.crop(cropSboxFirst=True):')
            show-[b.crop(cropSboxFirst=True) for b in canvas.bboxs]
            pblue('show Bboxs.cropSbox():')
            show-[b.cropSbox() for b in canvas.bboxs]
    
if __name__ == "__main__":
    pass
    
    
