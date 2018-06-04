# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from .ylimgTool import sk, np, sda
from .ylimgTool import (show, loga, mapp, normalizing, imsave, imread,
                       standImg, resize)

from ..ylcompat import py2

def base64Img(arr):
    import base64,cv2
    cnt = cv2.imencode('.jpg',arr[:,:,[2,1,0]])[1]
    if not py2:
        return base64.encodebytes(cnt[...,0]).decode('utf-8')
    return base64.encodestring(cnt)

def gifSave(imgs, name='a', fps=None,**kargs):
    '''
    图片序列 保存为GIF
    loop : int
        The number of iterations. Default 0 (meaning loop indefinitely)
    duration : {float, list}
        The duration (in seconds) of each frame. Either specify one value
        that is used for all frames, or one value for each frame.
    fps : float
        The number of frames per second. If duration is not given, the
        duration for each frame is set to 1/fps. Default 10.
    palettesize : int
        The number of colors to quantize the image to. Is rounded to
        the nearest power of two. Default 256.
    '''
    if name.lower()[-4:] != '.gif':
        name += '.gif'
    import imageio
    if fps :
        imageio.mimsave(name, imgs, fps=fps,**kargs)    
    else:
        imageio.mimsave(name, imgs,**kargs)    
        
def videoToImgs(videoPath,begin=0,end=0):
    import cv2
    cap = cv2.VideoCapture(videoPath)  
    if not cap.isOpened():
        raise NameError('video "%s" can\'t read by open CV !'%videoPath)
    number = 0
    frames = []
    while(cap.isOpened()):  
        ret, frame = cap.read()  
        if number>=begin:
            frame = frame[...,[2,1,0]]
            frames.append(frame)
        number+= 1
        if number >= end:
            break
    return frames
    
def generateBigImgForPaper(imgMa,lengh=1980,border=20,saveName='bigImgForPaper.png'):
    '''
    生成科研写作用的样本对比图
    imgMa: 图片行程的二维列表
    lengh: 大图片的宽度, 长度根据imgMa矩阵的高自动算出
    border: 图片与图片间的间隔
    '''
    big = None
    for rr in imgMa:
        rr = list(map(standImg,rr))
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
