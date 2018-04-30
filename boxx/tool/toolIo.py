# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

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