# -*- coding: utf-8 -*-
"""
code and data from:
    [PyTorch Transfer Learning tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

Download the data from
    `here <https://download.pytorch.org/tutorial/hymenoptera_data.zip>`_
    and extract it to the current directory.
"""
import os
import torch
from torchvision import datasets, transforms

data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

data_dir = 'hymenoptera_data'
data_dir = '/home/yanglei/tutorial/pytorch/hymenoptera_data'

image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['train', 'val']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=2,
                                             shuffle=True, num_workers=0)
              for x in ['train', 'val']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes

use_gpu = torch.cuda.is_available()


dataset = image_datasets['train']
dataloader = dataloaders['train']

if __name__ == '__main__':
    from boxx.ylth import *
    from boxx import tree, show
    tree - dataloaders
    show - dataloaders

    from boxx import torgb
    show(image_datasets, torgb)
