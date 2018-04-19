# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re, random
from os.path import join,isdir,isfile
from glob import glob

from .toolIo import openread,openwrite
from .toolLog import log

def filterList(key, strs):
    '''
    对一个str列表 找出其中存在字符串 key的所有元素
    '''
    return list(filter((lambda strr: key in strr),strs))

def findints(strr):
    '''
    返回字符串或字符串列表中的所有整数 ,r"\d+\d*"
    '''
    if isinstance(strr,(list,tuple)):
        return list(map(findints, strr))
    return list(map(int,re.findall(r"\d+\d*",strr)))

def randint(maxx=100):
    return random.randint(0, maxx)

def randfloat():
    return random.random()

def randchoice(seq, num=None):
    '''
    随机选择一个列表内的一个或num个元素
    '''
    if num is None:
        return random.choice(seq)
    return random.sample(seq, num)

def listdirWithFun(root='.',fun=None):
    '''对root路径及子路径下的每个path 执行fun
    
    Parameters
    ----------
    root : str, default '.'
        路径
    fun : funcation
        对每个子路径执行fun(path)
    '''
    paths = glob(join(root,'*'))
    for path in paths:
        if isdir(path):
            listdirWithFun(path,fun)
        if fun :
            fun(path)

def replaceAllInRoot(old, new, root='.', types='py'):
    '''对root路径及子路径下的每个types文件类型 执行替换old到new的操作 
    ps. old,new 应尽可能的长 包含更多的上下文信息 以避免错误的替换
    
    Parameters
    ----------
    old : str
        被替换部分
    new : str
        替换的新的内容
    root : str, default '.'
        路径 即根文件夹
    types : str or list, default 'py'
        需要被替换的文件类型
        str:单个类型, list:多个类型 默认为 'py'文件
    '''
    if not isinstance(types,(list,tuple)):
        types = [types]
    def replace(path):
        if isfile(path):
            if '.' in path and path.split('.')[-1] in types:
                code = openread(path)
                if old in code:
                    log('replaceAllInRoot: %s  old=%s  new=%s'%(path, old, new))
                    openwrite(code.replace(old,new),path)
    listdirWithFun(root, replace)
if __name__ == "__main__":
     
    string=["A001.45，b5，6.45，8.82",'sd4 dfg77']
    print(findints(string))
    pass