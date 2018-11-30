# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os, sys
import warnings
from functools import wraps

from ..ylsys import py2, sysi

class BoxxException(Exception):
    '''
    root Exception for boxx
    '''
    pass

class BoxxWarning(Warning):
    '''
    root warninng for boxx
    '''
    pass

class OffScreenWarning(BoxxWarning):
    pass

class Except():
    '''
    get traceback frame in with 
    
    >>> with excep:
    >>>     1/0
    >>> dira(excep)
    '''
    def __init__(self, deep=0):
        self.deep = deep
    def __enter__(self):
        pass
    def __exit__(self, typee, value, traceback):
        deep = self.deep
        while deep:
            deep -= 1
            traceback = traceback.tb_next
        self.type = typee
        self.value = self.v = value
        self.traceback = self.t = traceback
        self.frame = self.f = traceback.tb_frame
excep = Except()


def getExcept(fun):
    '''
    exec `fun()` and return (Exception, trace, frame)
    '''
    try:
        exc = Except(1) 
        with exc:
            fun()
    except Exception as ee:
        e = ee
        return e, exc.traceback, exc.frame
    
def warn(msg, warnType=BoxxWarning, filename=None, line=None, module='boxx', blue=False):
    '''
    log a warning of type warnType warn will auto fill filename and line 
    '''
    msg = '''%s
    %s'''%(('\x1b[36m%s\x1b[0m' if blue else '%s')% 'warning from boxx', msg)
    if filename is None or line is None:
        f = sys._getframe(1)
        c = f.f_code
        filename = c.co_filename if filename is None else filename
        line = c.co_firstlineno if line is None else line 
    warnings.warn_explicit(msg, warnType, filename, line, module)

warn1timeCache = {}
@wraps(warn)
def warn1time(msg, *l, **kv):
    '''
    log a warning of type warnType warn will auto fill filename and line 
    
    warn only one time
    '''
    if not warn1timeCache.get(msg):
        warn(msg, *l, **kv)
        warn1timeCache[msg] = True
    
getsize = os.path.getsize

def getsizem(path='.'):
    '''
    返回 path 的大小 支持文件夹 单位为 MB
    '''
    if os.path.isdir(path):
        return sum([getsizem(os.path.join(path, p)) for p in os.listdir(path)])
    return os.path.getsize(path)/float(1024**2)


def fileJoinPath(_file_,path='.'):
    '''
    返回 __file__ + 相对路径 path 后的绝对路径
    '''
    from os.path import abspath,join,dirname
    apath = abspath(join(dirname(abspath(_file_)),path))
    return apath

def filename(path):
    '''
    将路径和后缀名除去 只留下文件名字
    '''
    filen = name = os.path.basename(path)
    if '.' in name:
        filen = name[:name.rindex('.')]
    return filen

def listdir(path=None):
    path = path or '.'
    return os.listdir(path)

def openread(path, encoding='utf-8'):
    '''
    返回path文件的文本内容
    '''
    if py2:
        with open(path, 'r') as f:
            return f.read()
    with open(path, 'r', encoding=encoding) as f:
        strr = f.read()
    return strr
def openwrite(strr, path, mode='w', encoding='utf-8'):
    '''
    将strr写入path
    '''
    if py2:
        with open(path, mode) as f:
            f.write(strr)
        return path
    with open(path, mode, encoding=encoding) as f:
        f.write(strr)
    return path


def validFilename(filename, replaceBy='_'):
    '''
    return validate filename 
    '''
    import re
    if sysi.win:
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    else:
        rstr = r"[\/]" # ' / '
    newName = re.sub(rstr, replaceBy, filename)
    return newName

def loadjson(path):
    import json
    with open(path, 'r') as f:
        js = json.load(f)
    return js
def savejson(obj, path):
    import json
    with open(path, 'w') as f:
        json.dump(obj, f)
    return path 
    
def replaceTabInPy(dirr='.'):
    '''
    将所有tab换成4个空格
    '''
    from glob import glob
    from .toolLog import log
    pys = glob(os.path.join(dirr, '*.py'))
    for py in pys:
        code = openread(py)
        log(py,code.count('\t'))
        new = code.replace('\t',' '*4)
        openwrite(new, py)

def saveData(data, name='pickle_of_boxx', log=False):  #保存进度
    '''
    保存二进制数据
    '''
    import pickle
    if log:
        print('正在将数据写入',os.path.abspath('.'),'下的文件:“'+name+'”，请稍等。。。')
    with open(name, "wb") as f:
        pickle.dump(data,f)
    if log:
        print('\n文件“'+name+'”已保存在',os.path.abspath('.'),'目录下!')

def loadData(name='pickle_of_boxx', log=False):  #载入数据
    import pickle
    if not os.path.isfile(name):
        print('在',os.path.abspath('.'),'目录下,“'+name+'”文件不存在，操作失败！')
    if log:
        print('正在读取',os.path.abspath('.'),'目录下的文件:“'+name+'”\n请稍等。。。')
    with open(name,"rb") as f:
        data = pickle.load(f)
    f.close()
    if log:
        print('文件:“'+name+'”读取成功！')
    return data

def browserOpen(url):
    '''
    open url with browser
    if can't open browser raise warn
    '''
    import webbrowser
    if not webbrowser.open_new_tab(url):
        from boxx import warn
        warn('''can't open url with web browser, plaese open url:"%s" in your browser'''%url)
        
if __name__ == "__main__":

    pass