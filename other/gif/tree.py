from skimage.io import imread
img = imread('../../test/imgForTest/Lenna.jpg')

import torch
tensor = torch.rand((5, 1, 7))
complex_struct = {
    'str':'this is string! ^_^',
    'list':['img', img],
    'batch':{
        'tensor':tensor,
        'label':1,
            },
    'tuple_of_torch':tuple(tensor[0,0]),
        }
