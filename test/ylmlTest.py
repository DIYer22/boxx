# -*- coding: utf-8 -*-
from boxx import *
'''
使用`ifTest([funName]):`来判断是否执行测试
这样 在测试过程中可以在iPython 查看每一个变量
'''
img,gt = imread(pathjoin(dirname(__file__),'imgForTest/img.jpg')),imread(pathjoin(dirname(__file__),'imgForTest/gt_seg.png'))
gt = gt>0
# 多分类数据
gtm = np.zeros(img.shape[:2],img.dtype)
gtm[gt>.5] =1 
gtm[15:55] = 2
gtm[250:265] = 3
rem = gtm.copy()
rem[:,10:50] = 0
rem[:,100:150] = 1
rem[:,200:250] = 2
rem[:,300:350] = 3
colors = npa([[.5,.5,.5],[1,0,0],[0,1,0],[0,0,1],])
rec,gtc = (labelToColor(rem,colors),labelToColor(gtm,colors))

def ifTest(fun):
    shouldTest = fun is tests or (isinstance(tests,list) and fun in tests) or TEST_ALL 
    if shouldTest:
        try:
            pred('Test:'+ fun.__name__);log('Type:'+ str(type(fun)))
            log('Doc :'+ fun.__doc__)
        except Exception:
            pass
    return shouldTest

TEST_ALL = True
#TEST_ALL = False

testFun = None
tests = [testFun]

#tests = GenSimg
if (ifTest(GenSimg)) and 0:
    imgPath = 'G:\\experiment\\Data\\HKU-IS\\Imgs\\*.jpg'
    imggts = [(jpg,jpg.replace('.jpg','.png')) for jpg in  glob(imgPath)[:180]]
    simgShape = (100,100)
    cache = 6;batch = 3
    gen = GenSimg(imggts,simgShape,cache=cache,batch=batch)
    n=len(list(gen))
    print('实际的面积比值%d*%d=%d'%(n,batch,n*batch),'计算的一轮的总面积比值', 300*400/1e4*len(imggts))
    
    batch = 12
    gen = GenSimg(imggts,simgShape,cache=cache,batch=batch,timesPerRead=3)
    n=len(list(gen))
    print('timesPerRead=3实际的面积比值%d*%d=%d'%(n,batch,n*batch),'计算的一轮的总面积比值', 300*400/1e4*len(imggts))
    
    genn = GenSimg(imggts,simgShape,cache=cache,batch=batch,timesPerRead=3,iters=300)
    n=len(list(genn))
    print('iter=300实际的面积比值%d*%d=%d'%(n,batch,n*batch),'计算的一轮的总面积比值', 300)

    print('''检查随机性''')
    gen = GenSimg(imggts,simgShape,None,cache=2,batch=batch,iters=10)
    for ne in gen:
        show(ne[0])
    print(gen)

#tests = binaryDiff
if ifTest(binaryDiff):
    print('Tet binaryDiff')
    re = gt.copy()
    re[125:175] = 0
    re[:,250:300] = 1
    diff = binaryDiff(re,gt)
    show(re,gt)
    show(img,diff)


#tests = drawBoundAndBackground
if ifTest(drawBoundAndBackground):
    imgg = drawBoundAndBackground(greyToRgb(gt*255).astype(np.uint8),gt,img,size=.5)
    show(img,imgg)
    print('Test skimage.segmentation.find_boundaries,mark_boundaries!')
    from skimage.segmentation import find_boundaries,mark_boundaries
    #gt = (80<img[...,0])*img[...,0]<100
    #imgg = mark_boundaries(img,gt)
    imgg = find_boundaries(gt,mode='inner',background=1)
    show(img,imgg)

 
#tests = classDiff
if ifTest(classDiff):
    gtmod = classDiff(rem,gtm,colors)
    remod = classDiff(rem,gtm,colors,reMod=True)
    show(gtm,rem)
    show(gtc,rec)
    show(gtmod,remod)
    pass


#tests = confusionMatrix
if ifTest(confusionMatrix):
    gt = npa-[[1, 1, 3, 0],
           [0, 3, 0, 0],
           [0, 1, 2, 2],
           [2, 0, 2, 2]]
    re= gt.copy()
    re[0,0] = 0;classn = 4
    print(confusionMatrix(re,gt,classn))





#tests = f1Score
if ifTest(f1Score):
    gt = npa-[[1, 1, 3, 0],
           [0, 3, 0, 0],
           [0, 1, 2, 2],
           [2, 0, 2, 2]]
    re= gt.copy()
    re[0,0] = 0;classn = 4
    print('f1Score:',f1Score(re,gt,classn))




tests = autoSegmentWholeImg
if ifTest(autoSegmentWholeImg):
    simgShape=(100,100)
    core = getWeightCore(*simgShape)
    step = .2
    def f(img):
        img=img/255.
        return getWeightCore(*simgShape)[:,:,None]*img
    re=autoSegmentWholeImg(img, simgShape, handleSimg=f, step=step, weightCore=None)
    re2=autoSegmentWholeImg(img, simgShape, handleSimg=f, step=step, weightCore='gauss')
    re3=autoSegmentWholeImg(img, simgShape, handleSimg=f, step=step, weightCore='avg')
    show(img,re)
    show(re2,re3)
if __name__ == '__main__':
    pass




