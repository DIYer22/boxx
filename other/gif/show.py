
import numpy as np
from skimage.io import imread

img = imread('../../test/imgForTest/Lenna.jpg')

from boxx import show
show(img)
imgs = np.array([img, img, img])
show(imgs)
complex_struct = [dict(img=img, imgs=imgs)]
show(complex_struct)

from torch_data import dataloader
dataloader
show(dataloader)



from boxx import loga, torgb
# torgb is a funcation that 
# try to transfer a tensor to normalized RGB image
batch = next(iter(dataloader))[0]
loga(batch)
loga-torgb(batch)

show(dataloader, torgb)