# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import os
import random
from os.path import join,isdir,isfile
from glob import glob
from collections import defaultdict

from .toolIo import openread, openwrite, getsizem
from .toolLog import log

from ..ylsys import py2

intround = lambda floatt: int(round(floatt))

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
increase.d = __increase_recording
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
    return list(map(int,re.findall(r"-?\d+\d*",strr)))

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
    fun : function
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

def findinRoot(pattern='', root='.', maxsize=1, types=None, var=None, up=None, re=None, 
               exclude=None):
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
    var : str or bool, default None
        use re.compile('(^|[^a-zA-Z0-9_])%s([^a-zA-Z0-9_]|$)'%var) to find var name
    up : str or bool, default None
        Ignoring letter case of variable names
    re : str or bool, default None
        use re.compile(re) to search each line
    exclude : list , default ['pyc', 'swp', 'swo',]
        exclude file types in this list
    '''
    from re import compile as recompile
    if types is not None :
        if not isinstance(types,(list,tuple)):
            types = [types]
        types = [t.replace('.', '') for t in types]
    if exclude is None:
        exclude = []
    exclude += ['pyc', 'swp', 'swo', 'gz', 'whl', 'jpg', 'png', 'npz', 'bin']
    def intypes(path):
        typee = '.' in path and path.split('.')[-1].lower()
        if types is None:
            return typee not in exclude
        return typee in types
    if not pattern:
        pattern = var or up or re
    searchin = lambda strr: pattern in strr
    if var:
        pa = '''(^|[^a-zA-Z0-9_'"])%s([^a-zA-Z0-9_'"]|$)'''%pattern
        pa = recompile(pa)
        searchin = lambda strr: pa.search(strr)
    elif up:
        lower = pattern.lower()
        searchin = lambda strr: lower in strr.lower()
    elif re:
        pa = recompile(pattern)
        searchin = lambda strr: pa.search(strr)
    def find(path):
        if isfile(path):
            if (getsizem(path) <= maxsize or maxsize is None) and intypes(path):
                try:
                    s = openread(path)
                    if py2:
                        from .toolLog import tounicode
                        s = tounicode(s)
                    lines = [(i, l) for i,l in enumerate(s.split('\n'), 1) if searchin(l)]
                    if not len(lines):
                        return 
                    print('"%s" in "%s" with %s'%('\x1b[31m%s\x1b[0m'%pattern, '\x1b[36m%s\x1b[0m'%path, '\x1b[35m%s Lines\x1b[0m'%len(lines)))
                    for (i, l) in lines:
                        if l.startswith('   '):
                            l = '... '+l.strip()
                        if len(l) > 83:
                            l = l[:80] +' ...'
                        print('\t%s:%s'%('\x1b[35m%s\x1b[0m'%i, '\x1b[31m%s\x1b[0m'%l))
                    print("")
                except:
                    return 
    listdirWithFun(root, find)

def iscn(char):
    '''
    Does a char is chinese? 
    '''
    if u'\u4e00' <= char <= u'\u9fff':
        return True
    return False
    

def zipTar(paths, tarp):
    '''
    tar file for ,especially for label++
    '''
    import tarfile  
    with tarfile.open(tarp,'w') as tar:
        for path in paths:
            tar.add(path, arcname=os.path.basename(path))

def camel2snake(variable_name):
    s = variable_name[0].lower()
    for c in variable_name[1:]:
        if c.isupper():
            s += '_' + c.lower()
        else:
            s += c
    return s

def snake2camel(variable_name, lower_camel_case=False):
    s = variable_name[0].lower() if lower_camel_case else variable_name[0].upper()
    for idx, c in enumerate(variable_name[1:]):
        if variable_name[idx] == '_':
            s += c.upper()
        elif c != '_':
            s += c
    return s

if __name__ == "__main__":
     
    string=["A001.45，b5，6.45，8.82",'sd4 dfg77']
    print(findints(string))
    pass