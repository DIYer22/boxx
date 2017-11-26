# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from ylimgTool import cv2, sk, sio, np, plt, da
from ylimgTool import show, loga, mapp, normalizing, imsave, imread


def base64Img(arr):
    import base64,sys
    py3 = sys.version_info.major == 3
    cnt = cv2.imencode('.jpg',arr[:,:,[2,1,0]])[1]
    if py3:
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
        raise NameError,'video "%s" can\'t read by open CV !'%videoPath
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
    
if __name__ == '__main__':

    import pandas as pd
    df = pd.DataFrame({
                       0:range(5),
                       1:range(10,15),
                       'a':list("abcde"),
                       })
    df.set_index(0,inplace=True)
#    e = Evalu('sd','','%s')
#    e = Evalu('zd','','%s')
#    ed = Evalu.evalus

    pass
