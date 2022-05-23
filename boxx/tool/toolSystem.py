# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys, os, time
from ..ylsys import py2, tmpYl, sysi
from ..ylcompat import isstr, beforImportPlt, ModuleNotFoundError

from .toolIo import filename


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
    Only one import to support both environments : __name__ == '__main__' or in a package.
    And no need relative import.
        
    usage： 
        using: 
            >>> with impt():
            >>>     import local_py
        instead of :
            >>> if __name__ == '__main__':
            >>>     import local_py
            >>> else:
            >>>     from . import local_py
            
    Principle：
        temporary add the relpath in sys.path during with statement
        
    Parameters
    ----------
    relpath: str, default
        the dir path of the .py file that you want to import
        
    Zh-cn: 
        在包内或 __name__ == '__main__' 都能直接导入文件.
    '''
    from multiprocessing import Lock
    lock = Lock() # ensure work fine in multi-threading
    def __init__(self, relpath='.'):
        frame = sys._getframe(1)
        _file_ = frame.f_globals.get('__file__', "python_shell.py")
        dirr = os.path.dirname(_file_)
        self.d = os.path.abspath(os.path.join(dirr, relpath))
    def __enter__(self):
        with self.lock:
            sys.path.insert(0, self.d)
    def __exit__(self,*l):
        with self.lock:
            if sys.path[0] == self.d:
                assert sys.path.pop(0)==self.d, 'impt sys.path error'
            else:
                ind = sys.path.index(self.d)
                assert sys.path.pop(ind)==self.d, 'impt sys.path error'


class inpkg():
    '''
    inpkg = in package
    
    Execute relative import under __name__ == '__main__' enviroment in a package.
        
    usage： 
        using: 
            >>> with inpkg():
            >>>     from . import local_py
            
    Principle：
        auto search and import "top level package". Then, temporary replace __name__ to "module name under top level package" during with statement
        
    Zh-cn: 
        可以能直接运行包内含有 relative import code 的 py 文件
    '''
    def __init__(self):
        frame = sys._getframe(1)
        self.frame = frame
        self._file_ = frame.f_globals['__file__'] if '__file__' in frame.f_globals else frame.f_code.co_filename
        self._name_ = frame.f_globals['__name__']
        # NOTICE: second time %run will no '__package__' key
        self._package_ = self.frame.f_globals.get('__package__', None)  
        self.importTopLevelPackage = self._name_ == '__main__' or self._name_ == filename(self._file_)
        
    def findPackageRoot(self):
        dirr  = os.path.abspath(self._file_)
        files = []
        while len(dirr) > 1:
            files.append(filename(dirr))
            dirr = os.path.dirname(dirr)
            _init_p = os.path.join(dirr, '__init__.py')
            if not os.path.isfile(_init_p):
                return dirr, files
        raise Exception('Has __init__.py in root "/__init__.py"')
        
    def __enter__(self):
        if self.importTopLevelPackage:
            packageroot, files = self.findPackageRoot()
            if len(files) > 1:
                importByPath(os.path.join(packageroot, files[-1]))
            self.frame.f_globals['__name__'] = '.'.join(files[::-1])
            self.frame.f_globals['__package__'] = '.'.join(files[1:][::-1])
            
    def __exit__(self,*l):
        if self.importTopLevelPackage:
            self.frame.f_globals['__name__'] = self._name_
            if self._package_ is None:
                self.frame.f_globals.pop('__package__')
            else:
                self.frame.f_globals['__package__'] = self._package_


def importByPath(pyPath):
    '''
    import `.py` file by a python file path, return the py file as a moudle

    >>> module = importByPath('far/away.py')
    '''
    from boxx import os, dirname, sys, withfun
    pyFile = pyPath
    assert os.path.isfile(pyFile) or os.path.isdir(pyFile), pyFile
    dirr = dirname(pyFile)
    import importlib
    def exitFun(*l):
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
        self.log_str = name
        if callable(name):
            if "__qualname__" in dir(name):
                self.log_str = name.__qualname__
            elif "__name__" in dir(name):
                self.log_str = name.__name__

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
        s='\x1b[36m"%s" spend time: %s\x1b[0m'%(self.log_str, self.s)
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
    try:
        from pyheat import PyHeat
    except ModuleNotFoundError as e:
        print("Please pip install py-heat!")
        raise e
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
    try:
        float(s)
        return True
    except:
        return False

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
    os.makedirs(dirr, exist_ok=True)
    return dirr

def execmd(cmd, split=False):
    '''
    execuld cmd and reutrn str(stdout)
    '''
    with os.popen(cmd) as stream:
        if not py2:
            stream = stream._stream
        s = stream.read()
    if split:
        return s.strip().split('\n')
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