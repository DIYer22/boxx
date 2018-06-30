#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sample a small data set.
For each types files in dir, only copy 50 files to target.
won't copy size > 512MB file

Created on Sat Jun 30 14:58:44 2018

@author: yanglei
"""

import argparse, os
import shutil
from collections import defaultdict

from os.path import join, isdir, basename
pathjoin = join

parser = argparse.ArgumentParser(description="""
sample a small data set.
For each types files in dir, only copy 50 files to target.
won't copy size > 512MB file""")
parser.add_argument('source_target', nargs='*', default=None, type=str)
parser.add_argument('-n', default=10, type=float, 
                    help='How many data to copy')
parser.add_argument('-x', '--max', default=50, type=int, 
                    help='max numbers of the file if number > max: only copy top n file ')

parser.add_argument('-s', '--max_size', default=512, type=int, 
                    help="max size of the file if size > max_size won't copy, The unit is MB")


#parser.add_argument('source', nargs='*', default='boxx', type=str)
#parser.add_argument('target', nargs='0', default='/tmp/', type=str)


def path2type(path):
    if isdir(path):
        return "/dir"
    try:
        ind = path.rindex('.')
    except ValueError:
        return "/~."
    return path[ind+1:]

def filterFileList(l):
    if len(l) < arg.max:
        return l    
    n = arg.n
    if n < 1:
        n = len(l) * n
    n = int(n)
    l = sorted(l)
    return l[:n] 

def copyfile(src, dst):
    size = os.path.getsize(src)/float(1024**2)
    if size > arg.max_size:
        new = '%s_%sMB.fake'%(dst, int(size))
        with open(new ,'w',) as f:
            f.write('size = %s MB'%size)
        return 
    shutil.copyfile(src, dst)
    
def listdirWithFun(source='.', target='/tmp', __first=True):
    '''对source路径及子路径下的每个path 执行fun
    
    Parameters
    ----------
    source : str, default '.'
        路径
    fun : function
        对每个子路径执行fun(path)
    '''
    if __first:
        source = os.path.abspath(source)
        if isdir(target):
            target = pathjoin(target, basename(source))
        if not isdir(target):
            os.makedirs(target)    
        
#    paths = [pathjoin(source, p) for p in os.listdir(source)]
    paths = os.listdir(source)
    
    d = defaultdict(lambda :[])
    [d[path2type(pathjoin(source, p))].append(p) for p in paths]
    
    d = {k:filterFileList(v) for k,v in d.items()}
    
    dirs = d.pop('/dir') if '/dir' in d else []
    
    [[copyfile(pathjoin(source, p), pathjoin(target, p))  for p in l] for l in d.values()]
    
    for dirr in dirs:
        targetd = pathjoin(target, dirr)
        if not isdir(targetd):
            os.makedirs(targetd)
        listdirWithFun(pathjoin(source, dirr), target=targetd, __first=False)

if __name__ == '__main__':
    arg = parser.parse_args()
    arg.max = max(arg.max, arg.n)
    arg.source = arg.source_target[0] if len(arg.source_target) else '.'
    arg.target = arg.source_target[1] if len(arg.source_target)>=2 else '/tmp/'
    print(arg)
    listdirWithFun(arg.source, arg.target)





