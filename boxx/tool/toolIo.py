# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os, sys
import warnings

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
    name = os.path.basename(path)
    filen = name[:name.rindex('.')]
    return filen

def listdir(path=None):
    path = path or '.'
    return os.listdir(path)

def openread(path):
    '''
    返回path文件的文本内容
    '''
    with open(path, 'r') as f:
        strr = f.read()
    return strr
def openwrite(strr, path, mode='w'):
    '''
    将strr写入path
    '''
    with open(path, mode) as f:
        f.write(strr)
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

if __name__ == "__main__":

    pass