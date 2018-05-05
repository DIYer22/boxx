# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re, random
from os.path import join,isdir,isfile
from glob import glob
from collections import defaultdict

from .toolIo import openread, openwrite, getsizem
from .toolLog import log


__increase_recording = defaultdict(lambda:-1)
def increase(namespace=None):
    '''
    从0开始 每调用一次返回的数值自增 1， 类似 SQL 中的 AUTO_INCREMENT 字段
    
    Parameters
    ----------
    namespace : hashable, default None
        用于计数的命名空间
    '''
    __increase_recording[namespace] += 1
    return __increase_recording[namespace]
    
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

def findinRoot(pattern, root='.', maxsize=1, types=None):
    '''
    在root及子路径下的所有文件中 查找 pattern。存在 则打印出对应文件的那一行。
    
    Parameters
    ----------
    pattern : str
        要查找的内容
    root : str, default '.'
        路径 即根文件夹
    maxsize : number, default 1
        被查找文件的最大文件大小，单位为 MB
        为避免不小心查找太大的二进制文件，默认不超过 1MB
        设为 None，则不设大小限制
    types : str or list, default None
        被查找文件的类型限制
        str:单个类型, list:多个类型 默认为所有文件
    '''
    if types is not None :
        if not isinstance(types,(list,tuple)):
            types = [types]
        types = [t.replace('.', '') for t in types]
    def intypes(path):
        if types is None:
            return True
        return '.' in path and path.split('.')[-1] in types
    
    def find(path):
        if isfile(path):
            if (getsizem(path) <= maxsize or maxsize is None) and intypes(path):
                try:
                    s = openread(path)
                    if pattern in s:
                        lines = [(i, l) for i,l in enumerate(s.split('\n'), 1) if pattern in l]
                        print('"%s" in "%s" with %s'%('\x1b[31m%s\x1b[0m'%pattern, '\x1b[36m%s\x1b[0m'%path, '\x1b[35m%s Lines\x1b[0m'%len(lines)))
                        for (i, l) in lines:
                            if l.startswith('   '):
                                l = '... '+l.strip()
                            if len(l) > 83:
                                l = l[:80] +' ...'
                            print('\t%s:%s'%('\x1b[35m%s\x1b[0m'%i, '\x1b[31m%s\x1b[0m'%l))
                        print()
                except:
                    return 
    listdirWithFun(root, find)
    
if __name__ == "__main__":
     
    string=["A001.45，b5，6.45，8.82",'sd4 dfg77']
    print(findints(string))
    pass