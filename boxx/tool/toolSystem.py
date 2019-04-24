# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys, os, time
from ..ylsys import py2, tmpYl, sysi
from ..ylcompat import isstr, beforImportPlt, ModuleNotFoundError


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
        
def importByPath(pyPath):
    '''
    import `.py` file by a python file path, return the py file as a moudle

    >>> module = importByPath('far/away.py')
    
    TODO 增加对 module 的支持
    '''
    from boxx import os, dirname, sys, withfun
    pyFile = pyPath
    assert os.path.isfile(pyFile), pyFile
    dirr = dirname(pyFile)
    import importlib
    def exitFun():
        assert sys.path.pop(0)==dirr
    with withfun(lambda :sys.path.insert(0, dirr), exitFun):
        module = importlib.import_module(os.path.basename(pyFile).replace('.py',''))
        return module
    
def tryImport(moduleName):
    '''
    try `import @moduleName`. if @moduleName is not installed, return a FakeModule to placeholder the module name
    '''
    module = None
    try:
        exec('import %s as module' % moduleName)
        return module
    except (ModuleNotFoundError, ImportError):
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

def removeImportSelf(modelName='boxx.out'):
    '''
    remove a model while import itself
    that mean every time import model will exec model again
    
    Notice: Only support Python 3, For Python 2 only first time import works 
    '''
    if py2 :
        return 
    sys.modules.pop(modelName)
    
    f = sys._getframe(4)
    if 'spec' in f.f_locals:
        f.f_locals['spec'].name = 'sys'

def removeimp(modulesName='boxx'):
    '''
    remove all module by name
    '''
    [sys.modules.pop(k) for k,v in list(sys.modules.items()) if k.startswith(modulesName + '.') or k == modulesName]

def crun(pycode, snakeviz=True):
    '''
    use snakeviz and cProfile to analyse the code performance
    a visualization flame graph web page will be opened in your web browser
    
    Parameters
    ----------
    pycode : str
        Python code
    snakeviz : bool, default True
        use snakeviz to get flame graph in web page
        otherwise, print cProfile result sorted by time
    '''
    from cProfile import run

    if not snakeviz:
        return run(pycode,sort='time')
    import webbrowser
    if not webbrowser.open(''):
        from boxx import warn
        msg = '''**Can't detect browser** in operating environment.
so, we use cProfile.run(pycode,sort='time'),
instead of using snakeviz to visualization code perfomance in web page'''
        warn(msg)
        run(pycode,sort='time')
        print('\n\n'+msg)
        return 
    run(pycode, os.path.join(tmpYl, "snakeviz.result"))
    if not sysi.win:
        from . import softInPath
        assert softInPath('snakeviz'),'run `pip install snakeviz`'
        os.system('snakeviz %s &'% os.path.join(tmpYl,'snakeviz.result'))
    elif sysi.win:
        os.system('start /b  snakeviz.exe %s '% os.path.join(tmpYl,'snakeviz.result'))
        
    
def performance(pyfileOrCode, snakeviz=True):
    '''
    use snakeviz and cProfile to analyse the python file or python code performance
    a visualization flame graph web page will be opened in your web browser
    
    Parameters
    ----------
    pyfileOrCode : str
        Python file's path or python code
    snakeviz : bool, default True
        use snakeviz to get flame graph in web page
        otherwise, print cProfile result sorted by time
    '''
    if pyfileOrCode.endswith('.py'):
        crun("from boxx import runpyfile;runpyfile('%s')"%pyfileOrCode)
    else:
        crun(pyfileOrCode)

class timeit():
    '''
    usage 1 :
        >>> with timeit():
        >>>     fun()
    usage 2 :
        >>> ti = timeit()
        # run your code
        >>> print ti()
        
    P.S `with timeit(0)` will convenient stop print 
    '''
    def __init__(self,name='timeit'):
        self.last = self.begin = time.time()
        self.log = isstr(name) or bool(name)
        self.key = name
    def __call__(self):
        '''返回时间差'''
        t = time.time()
        r = t -self.last
        self.last = t
        return r
    def __enter__(self):
        return self
    def __exit__(self, typee, value, traceback):
        self.t = time.time()-self.begin
        self.p
    @property
    def s(self):
        from .toolLog import strnum
        if 't' not in self.__dict__:
            self.t = self()
        return strnum(self.t,6)
    def __str__(self):
        s='\x1b[36m"%s" spend time: %s\x1b[0m'%(self.key, self.s)
        return s
    @property
    def p(self):
        '''直接打印出来'''
        if self.log:
            print(self)


def heatmap(pathOrCode):
    '''show the heatmap of code or python file
    if raise UnicodeDecodeError in Python 2 which may cause by Chinese, Japaneses
    then will replace all symbol not belong ascii to "?$"
    
    Parameters
    ----------
    pathOrCode : str
        .py file path or Python code
    
    Chinese:
    会让代码里面的中文全部失效
    
    Parameters
    ----------
    pathOrCode : str of code or path of .py
        .py文件路径或着python代码
    '''
    beforImportPlt()
    from pyheat import PyHeat
    import matplotlib.pyplot as plt
    tmppath = 'code-tmp-pyheat-boxx.py'
    
    ispath = pathOrCode.endswith('.py')
    path = pathOrCode if ispath else tmppath
    try :
        if not ispath:
            with open(tmppath,'w') as f:
                f.write(pathOrCode)
        ph = PyHeat(path)
        ph.create_heatmap()
        ph.show_heatmap()
    except UnicodeDecodeError:
        plt.show()
        msg = '''UnicodeDecodeError! try to replace not ascii symbol to '$?' and retry'''
        from boxx import warn
        warn(msg)
        
        with open(path) as f:
            code = f.read()
        code = code.decode('ascii','replace').replace('\ufffd','$?')
        with open(tmppath,'w') as f:
            f.write(code.encode('utf-8'))
        
        ph = PyHeat(tmppath)
        ph.create_heatmap()
        ph.show_heatmap()
    finally:
        if os.path.isfile(tmppath):
            os.remove(tmppath)

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
    for p in os.environ['PATH'].split(';' if sysi.win else ':'):
        if os.path.isdir(p) and softName in os.listdir(p):
            return True
    return False

def makedirs(dirr, randomDelay=0.0001):
    if os.path.isdir(dirr):
        return dirr
    from random import random
    time.sleep(random()*randomDelay)
    if os.path.isdir(dirr):
        return dirr
    os.makedirs(dirr)
    return dirr

def execmd(cmd):
    '''
    execuld cmd and reutrn str(stdout)
    '''
    with os.popen(cmd) as stream:
        if not py2:
            stream = stream._stream
        s = stream.read()
    return s

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



mainFrame = []
def getMainFrame(frame=0):
    '''
    return a main frame from father frames that first frame.f_locals['__name__'] == '__main__' 
    
    Parameters
    ----------
    frame : frame or int, default 0
        if int:相对于调用此函数frame的 int 深度的对应frame
    '''
    if len(mainFrame):
        return mainFrame[0]
    fs = getFatherFrames(frame=frame+1, endByMain=True)
    main = fs[-1]
    mainFrame.append(main)
    return main
getMainFrame()


rootFrame = []
def getRootFrame():
    '''
    return interactive frame
    '''
    if len(rootFrame):
        return rootFrame[0]
    frame=0
    endByMain=False
    fs = getFatherFrames(frame=frame+1, endByMain=endByMain)
    root = getMainFrame()
    
    for f in fs:
        if f.f_code.co_filename.startswith('<ipython-input-'):
            root = f
            break
    rootFrame.append(root)
    return root
getRootFrame()

if __name__ == "__main__":

    pass