# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys, os, time
from ..ylsys import py2, tmpYl
from ..ylcompat import isstr


def importAllFunCode(mod=None):
    '''
    mod 为包名(type(mod)=='str')或包本身(type(mod)==module)
    自动生成导入所有模块语句 并过滤掉__name__等
    '''
    if mod is None:
        mod = 'yllab'
    if isinstance(mod,str):
        exec ('import %s as mod'%mod)

    names = [name for name in dir(mod) if not ((len(name)>2 and name[:2]=='__') or 
                                  name in ['unicode_literals',])]
    n = 5
    lines = []
    while len(names) > n:
        l,names = names[:n],names[n:]
        lines += [', '.join(l)]
    lines += [', '.join(names)]
    lines = ',\n          '.join(lines)
    
    strr = (("from %s import *\n    from %s import (%s)"%(mod.__name__,mod.__name__,lines)))
    strr = '''from %s import *
try:
    from %s import (%s)
except ImportError:
    pass'''%(mod.__name__,mod.__name__,lines)
    print(strr)

class impt():
    '''
    使Python 3 在包内可直接 import. 并且， 可直接运行包内的文件.
    原理：
        enter时候 append __file__, exit时候 pop
    用法：  
        with impt(__file__):
            from tool import *
    '''
    def __init__(self, _file_):
        self.f = _file_
    def __enter__(self):
        sys.path.append(self.f)
    def __exit__(self,*l):
        assert sys.path.pop() == self.f, 'impt sys.path error'
        
        
def tryImport(moduleName):
    '''
    try `import @moduleName`. if @moduleName is not installed, return a FakeModule to placeholder the module name
    '''
    
    notFoundError = ModuleNotFoundError if not py2 else ImportError
    module = None
    try:
        exec('import %s as module' % moduleName)
        return module
    except (notFoundError, ImportError):
        return  '''"%s" is not install in your Python Enveroment! 
This is a fake one. Please install "%s" and retry''' % (moduleName, moduleName)
        return FakeModule(moduleName)
__FAKE_DIC__ = {}
class FakeModule():
    '''
    a fake Module to placeholder the module name that some module may not installed.
    once use this module, will raise ImportError
    '''
    def __init__(self, name):
        __FAKE_DIC__[id(self)] = '"%s" is not install in your Python Enveroment! This is a fake one. Please install "%s" and retry' % (name, name)
    def __getattribute__(self, name=None, *l):
        raise ImportError(__FAKE_DIC__[id(self)])
    def __getattr__(self, name):
        raise ImportError(__FAKE_DIC__[id(self)])
    def __setattr__(self, name, v, *l):
        raise ImportError(__FAKE_DIC__[id(self)])
    def __str__(self):
        errorMsg = __FAKE_DIC__[id(self)]
        raise ImportError(errorMsg)
    __repr__ = __str__
        
def crun(pycode, snakeviz=True):
    '''测试代码pycode的性能'''
    from cProfile import run
    if not snakeviz:
        return run(pycode,sort='time')
    run(pycode, os.path.join(tmpYl, "snakeviz.result"))
    from . import softInPath
    assert softInPath('snakeviz'),'run `pip install snakeviz`'
    os.system('snakeviz %s &'% os.path.join(tmpYl,'snakeviz.result'))
    
    
def frun(pyFileName=None):
    '''在spyder中 测试pyFileName的性能'''
    if pyFileName:
        if '.py' not in pyFileName:
            pyFileName += '.py'
        crun("runfile('%s',wdir='.')"%pyFileName)
    else:
        crun("runfile(__file__,wdir='.')")

class timeit():
    '''
    记时 :
        >>> ti = timeit()
        # run your code
        >>> print ti()
    记时2 :
        >>> with timeit():
        >>>     fun()
        加个 0 即可方便地关闭计时，即 with timeit(0)
    
    测试code时间 :
        >>> timeit(your_code)
    '''
    def __init__(self,code=''):
        self.begin = time.time()
        self.log = isstr(code) or bool(code)
        if isstr(code):
            if len(code):
                exec(code)
                print(self.s)
    def __call__(self):
        '''返回时间差'''
        return time.time()-self.begin
    def __enter__(self):
        return self
    def __exit__(self, typee, value, traceback):
        self.p
    @property
    def s(self):
        t = time.time()-self.begin
        s='\x1b[36mspend time: %s\x1b[0m'%t
        return s
    @property
    def p(self):
        '''直接打印出来'''
        if self.log:
            print(self.s)

def heatMap(pathOrCode):
    '''显示python代码的时间热力图
    ps.会让代码里面的中文全部失效
    
    Parameters
    ----------
    path : str of code or path of .py
        .py文件路径或着python代码
    '''
    from pyheat import PyHeat
    path = os.path.join(tmpYl, 'pyheat-tmp.py')
    code = pathOrCode
    try :
        if os.path.isfile(pathOrCode):
            path = pathOrCode+'_HEAT_MAP_TMP.py'
            with open(pathOrCode) as f:
                code = f.read()
        if py2:
            code = code.decode('ascii','replace').replace('\ufffd','$?')
        with open(path,'w') as f:
            f.write(code)
        ph = PyHeat(path)
        ph.create_heatmap()
        ph.show_heatmap()
    finally:
        if os.path.isfile(path):
            os.remove(path)
        
def strIsInt(s):
    '''判断字符串是不是整数型'''
    s = s.replace(' ','')
    return s.isdigit() or (s[0]==('-') and s[1:].isdigit())

def strIsFloat(s):
    '''判断字符串是不是浮点'''
    s = s.replace(' ','')
    return s.count('.')==1 and strIsInt(s.replace('.',''))
def strToNum(s):
    ''' 若字符串是float or int 是则返回 数字 否则返回本身'''
    if strIsInt(s):
        return int(s)
    if strIsFloat(s):
        return float(s)
    return s

def getArgvDic(argvTest=None):
    '''
    将cmd的`python main.py arg1 arg2 --k v --tag`形式的命令行参数转换为(list, dict)
    若v是数字 将自动转换为 int or float, --tag 将表示为 dic[tag]=True
    
    Return
    ----------
    l : list
        去除第一个参数 文件地址外的 第一个 '--'之前的所有参数
    dic : dict
        `--k v` 将以{k: v}形式存放在dic中
        `--tag` 将以{k: True}形式存放在dic中
    '''
    from .toolLog import  pred
    argv = sys.argv
    if argvTest:
        argv = argvTest
    l = argv = list(map(strToNum,argv[1:]))
    code = [(isinstance(x,str) 
        and len(x) >2 and x[:2]=='--') for x in argv]
    dic = {}
    if True in code:
        l = argv[:code.index(True)]
        n = len(code)
        for i,s in enumerate(code):
            x = argv[i]
            if int(s):
                k = x.replace('--','')
                if (i<=n-2 and code[i+1]) or i==n-1: # 不带参数
                    dic[k] = True
                else:  # 带参数
                    dic[k] = argv[i+1]
    if len(dic) or len(l):
        pred('command-line arguments are:\n  %s and %s'%(l,dic))
    return l,dic


def softInPath(softName):
    '''
    是否安装命令为softName的软件，即 判断softName 是否在环境变量里面
    '''
    for p in os.environ['PATH'].split(':'):
        if os.path.isdir(p) and softName in os.listdir(p):
            return True
    return False

def addPathToSys(_file_, pathToJoin='.'):
    '''
    将 join(__file__, pathToJoin)  加入 sys.path

    Parameters
    ----------
    _file_ : str
        .py 文件的路径 即__file__ 变量
    pathToJoin : str, default '.'
        相对路径
    '''
    from os.path import abspath,join,dirname
    apath = abspath(join(dirname(abspath(_file_)),pathToJoin))
    if apath not in sys.path:
        sys.path.append(apath)
    return apath

def getFatherFrames(frame=0, endByMain=True):
    '''
    返还 frame 的所有的父 frame 即 Call Stack
    
    Parameters
    ----------
    frame : frame or int, default 0
        if int:相对于调用此函数frame的 int 深度的对应frame
    endByMain : bool, default True
        为 True 则在第一个 frame.f_locals['__name__'] == '__main__' 处停止搜寻
        目的是去除 IPython 自身多余的 Call Stack
    '''
    if frame is False and endByMain:
        frame, endByMain = 0, False
    if isinstance(frame, int):
        frame = sys._getframe(1 + frame)
    fs = []
    while frame:
        fs.append(frame)
        if endByMain:
            if '__name__' in frame.f_locals and frame.f_locals['__name__'] == '__main__':
                break
        frame = frame.f_back
    return fs

def getRootFrame(frame=0, endByMain=True):
    '''
    返还 frame 的root frame 即 interactive 所在的 frame
    
    Parameters
    ----------
    frame : frame or int, default 0
        if int:相对于调用此函数frame的 int 深度的对应frame
    endByMain : bool, default True
        为 True 则在第一个 frame.f_locals['__name__'] == '__main__' 处停止搜寻
        目的是去除 IPython 自身多余的 Call Stack
    '''
    fs = getFatherFrames(frame=frame+1, endByMain=endByMain)
    return fs[-1]


if __name__ == "__main__":

    pass