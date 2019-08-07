# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from .toolStructObj import addCall, dicto, FunAddMagicMethod, getfathers, typeNameOf, typestr
from .toolSystem import getRootFrame, getFatherFrames
from ..ylsys import py2
from ..ylcompat import printf, unicode
from ..ylcompat import istype

import os,sys,time
import math
import re
from collections import defaultdict

def localTimeStr():
    '''
    获得本地时间(GM+8 北京时间)
    '''
    return time.asctime( time.localtime(time.time()))
def gmtTimeStr():
    '''
    获得gmt时间(GM0 格林威治时间)
    '''
    return time.asctime(time.gmtime(time.time()))


class timeGap:
    '''
    定时log器 隔固定的一段时间 返回 当前轮数(True)
    
    Init Parameters
    ----------
    gap : float
        隔多少秒返回一个 True
    fun : function, default None
        每一次要执行fun()
    quickBegin : bool, default True
        First time call will return True
    
    Attribute
    ----------
    __call__ : 
        返还 当前轮数(True)
    time : @property
        is @property 返回已记录的时长
    '''
    def __init__(self, gap=1,fun=False, quickBegin=True):
        self.n = 0
        self.gap = gap
        self.begin = time.time()
        self.last = self.begin - (quickBegin and gap)
        self.fun = fun
    def __call__(self,):
        t = time.time()
        if t - self.last >= self.gap:
            self.last = t
            self.n += 1
            if self.fun:
                self.fun()
            return self.n
        return False
    @property
    def time(self):
        return time.time() - self.begin

TimeGapDic = {}
def timegap(gap=10, key='boxx.default'):
    '''
    定时器 隔固定的一段时间 返回 当前轮数(True), use to log in loop
    This is light version of timeGap, for More Infomation help(timeGap)
    
    Init Parameters
    ----------
    gap : number
        隔多少秒返回一个 True
    key : hashable, default 'boxx.default'
        the namespace to count
    '''
    keyt = (gap, key)
    if keyt not in TimeGapDic:
        TimeGapDic[keyt] = timeGap(gap)
    return TimeGapDic[keyt]()

__logGapDic = {}
def logGap(key='gap'):
    '''
    log time gap in loop
    '''
    d = __logGapDic
    l = d.get(key)
    now = time.time()
    if not l :
        pblue('Begin to log time gap of "%s"!'%key)
        d[key] = [0, now]
    else :
        dt = now - l[1]
        pblue('%dst loop, "%s" spend %ss.'%(l[0] ,key, strnum(dt)))
        l[0] += 1
        l[1] = now

frontColorDic = dicto({   # 前景色
        'black'    : 30,   #  黑色
        'red'      : 31,   #  红色
        'green'    : 32,   #  绿色
        'yellow'   : 33,   #  黄色
        'blue'     : 34,   #  蓝色
        'purple'   : 35,   #  紫红色
        'cyan'     : 36,   #  青蓝色
        'white'    : 37,   #  白色
    })
class colorFormat:
    '''
    同时兼容windows和Linux及各类明暗色调的颜色str temple
    只有 red, cyan(==blue), purple
    使用colorFormat.printAllColor()查看效果
    用法: print colorFormat.blue%strr
    '''
    red = '\x1b['+str(frontColorDic['red'])+'m%s\x1b[0m'
    cyan= '\x1b['+str(frontColorDic['cyan'])+'m%s\x1b[0m'
    purple = '\x1b['+str(frontColorDic['purple'])+'m%s\x1b[0m'
    black = '\x1b['+str(frontColorDic['black'])+'m%s\x1b[0m'
    blue = cyan
    info = blue
    danger = red
    err = red
    b = blue
    r = red
    p = purple
    @staticmethod
    def printAllColor(s='printAllColor'):
        return [stdout((c+' '*10)[:7]) and pcolor(c,": "+str(s)) for c in frontColorDic] and None
    pall = printAllColor
clf = colorFormat

def decolor(colored):
    '''
    remove color of str
    '''
    pa = re.compile('\x1b\[3[0-9]m|\x1b\[0m')
    new = pa.sub('', colored)
    new = pa.sub('', new)
    return new

def tounicode(strr):
    '''
    Python2 中文编码错误解决方案，用于代替str类及函数, 全部换成unicode
    '''
    if not py2:
        if isinstance(strr,str):
            return strr
        if isinstance(strr,bytes):
            return strr.decode('utf-8','replace')
        return str(strr)
    else:
        if isinstance(strr,unicode):
            return strr
        strr = str(strr)
        if isinstance(strr,str):
            return strr.decode('utf-8','replace')
        return unicode(strr)

def tostrpy2(x):
    '''
    only work py2 return a str to avoid 
    UnicodeEncodeError when `str(u'中文')`
    '''
    if not py2:
        return str(x)
    if isinstance(x,unicode):
        return x.encode('utf-8','replace')
    s = str(x)
    return s

def shortDiscrib(x):
    '''
    short Discrib of anything for logc number is better 
    '''
    if isinstance(x, int):
        return str(x)
    typee = typestr(x)
    from ..ylimg import StructLogFuns
    fund = StructLogFuns
    f = shortStr
    if typee in fund:
        f = fund[typee]
        if 'torch.' in typee and 'ensor' in typee and (not x.shape):
            f = strnum
    elif '__float__' in dir(x):
        try:
            x = float(x)
            f = strnum
        except:
            pass
    try:
        return decolor(f(x))
    except:
        return str((x))

def shortStr(x, maxlen=60):
    '''
    genrate one line discrib str shorter than maxlen.
    if len(s)> maxlen then slice additional str and append '...' 
    BTW. function will replace '\n' to '↳'
    
    if bool(maxlen) is False, not be short
    '''
    s = tounicode(x).strip()
    if maxlen and len(s) > maxlen:
        s = s[:maxlen-3]
        s +=  '...'
        if '\x1b[' in s :
            s += '\x1b[0m' * (list(s).count('\x1b'))
    s = s.replace('\n','↳')
    return s

def discrib(x, maxline=20):
    '''
    return discrib of x less than maxline.
    if len(s)> maxline*80 then slice additional str and append '...' 
    
    if bool(maxline) is False, return s
    '''
    s = tounicode(x)
    if not maxline:
        return s
    enters = s.count('\n')+1
    n  = len(s)
    maxlen = maxline * 80
    if n > maxlen:
        s = s[:maxlen-6]+'......'
    elif enters > maxline:
        s = '\n'.join(s.split('\n')[:maxline]) + '\n......'
    else:
        return s
    if '\x1b[' in s :
        s += '\x1b[0m' * (list(s).count('\x1b'))
    return s


def logc(code, exe=None):
    '''
    short of log code
    pretty print expression by show every var's value in expression
    
    Parameters
    ----------
    code : str
        the expression code that want to print
    exe : bool, default None
        wether exec(code) befor print
        when exe is None:
            try not exec(code)
            but if some var in expression can't find in locals() and globls()
                then exec(code)
    
    TODO:
        1. use re to replace vars name avoid the same names
        2. use Abstract Syntax Tree and re 
           to distinguish .attr, function call []
    '''
    frame = sys._getframe(2)
    local = frame.f_locals
    glob = frame.f_globals
    
    if exe:
        exec(code, local, glob)
    
    varss = re.findall('[a-zA-Z_][a-zA-Z0-9_]*',code)
    dic = {}
    for name in varss:
        if name in local:
            dic[name] = local[name]
        elif name in glob:
            dic[name] = glob[name]
        elif exe is None:
            exec(code, local, glob)
            if name in local:
                dic[name] = local[name]
            else:
                dic[name] = addCall(name)
    coder = numr = code
    
    toNotVarName = lambda name: '$_%s_$'% ''.join([str(ord(c)) for c in name])
    addSpaceBothSide = lambda s, n: (n//2)*' ' + str(s) + (n-n//2)*' '
    
    for k, v in sorted(dic.items(), key=lambda x:-len(x[0])):
        vstr = shortDiscrib(v)
        if callable(v):
            vstr = k
        maxs = max(len(vstr), len(k))
        
        dic[k] = dict(
                vstr=vstr,
                maxs=maxs,
                v=v,
                ks=addSpaceBothSide(k, maxs-len(k)),
                vs=addSpaceBothSide(vstr, maxs-len(vstr)),
                )
        coder = coder.replace(k, toNotVarName(k))
        numr = numr.replace(k, toNotVarName(k))
    
    for k, d in sorted(list(dic.items()), key=lambda x:-len(x[0])):
        coder = coder.replace(toNotVarName(k), clf.b%d['ks'])
        numr = numr.replace(toNotVarName(k), clf.r%d['vs'])
    
    s = ('Code: %s\n  └── %s'%(coder, numr))   
    print(s)
logc = FunAddMagicMethod(logc)

def tabstr(s, head=4, firstline=False):
    '''
    to tab a block of str for pretty print
    
    Parameters
    ----------
    head : str or int, default 4
        the str that to fill the head of each line
        if value is int, head = ' '*head
    firstline : bool, default False
        whether fill the first line 
    '''
    if isinstance(head, int):
        head = ' '*head
    if firstline:
        s = head + s
    return s.replace('\n','\n'+head)

def getDoc(f):
    '''
    get document of f, if f don't have __doc__, return None
    '''
    if '__doc__' in dir(f) and f.__doc__:
        return f.__doc__
    return None
        
def pcolor(color, *s):
    '''
    用颜色打印 不返回
    '''
    if not isinstance(color,int):
        color = frontColorDic[color]
    print(('\x1b[%dm%s\x1b[0m'%(color, ' '.join(map(tounicode,s)))))
    return 
    if len(s) == 1:
        return s[0]
    return s
pcyan = lambda *s:pcolor('cyan',*s) #  青蓝色
pred = lambda *s:pcolor('red',*s) #  红色
ppurple = lambda *s:pcolor('purple',*s) #  紫红色
pblue = pcyan 

def stdout(*l):
    sys.stdout.write(('%s'%(' '.join(map(tounicode,l)))))
    if len(l) == 1:
        return l[0]
    return l

class Log():
    def __call__(self,*l, **kv):
        printf(*l, **kv)
    def __div__(self, x):
        printf(x)
        return x
    __sub__ = __call__
    __truediv__ = __div__
log = FunAddMagicMethod(printf)
printt = log

def printToStr(value='', *l, **kv):
#def printToStr(value='', *l, sep=' ', end='\n', file=None, flush=False): # for py version < 2.7.16
    '''
    same usage to print function, but replace stdout to return str
    '''
    sep=' '
    end='\n'
    file=None
    flush=False
    locals().update(kv)
    l = (value,)+l
    s = sep.join([tounicode(v) for v in l]) + end
    return s

class PrintStrCollect():
    from functools import wraps
    def __init__(self, ):
        self.s = ''
    @wraps(printToStr)
    def __call__(self, *l, **kv):
        s = printToStr(*l, **kv)
        self.s += s
    def __str__(self):
        s = self.s
        return tostrpy2(s)
    pass

class LogAndSaveToList(list):
    '''
    存储最近用于logg的结果, 并返回x的class, list版本SuperG
    '''
    def __init__(self,printFun=None,cache=5):
        self.p = printFun or pblue
        self.cache = cache
    @property
    def i(self):
        return self[-1]
    _ = i
    @property
    def ii(self):
        return self[-2]
    __ = ii
    @property
    def iii(self):
        return self[-3]
    ___ = iii
    @property
    def iiii(self):
        return self[-4]
    ____ = iiii
    def __call__(self,*l,**dic):
        while self.cache < len(self):
            self.remove(self[0])
        if len(l) == 1:
            self.p(l[0])
            self.append(l[0])
            return l[0]
        self.p('\n'.join(map(tounicode,l)))
        if len(dic):
            for k in dic:
                self.p('%s = %s'%(k,tounicode(dic[k])))
            self.append(dic)
        self.append(l)
        return l
    __sub__ = __lshift__ = __rshift__  = __div__ = __truediv__ =__call__
    def __repr__(self):
        blue  = '\x1b[%dm%s\x1b[0m'%(frontColorDic['red'],tounicode(len(self) and self[len(self)-1]))
        return '''LogAndSaveToList(printFun=%s, cache=%s) log[-1]: %s'''%(
        str(self.p),self.cache,blue)
    __str__ = __repr__

logg = LogAndSaveToList()
pcyan,pred,ppurple,stdout = list(map(FunAddMagicMethod,
                                        [pcyan,pred,ppurple,stdout]))
    
pblue = pcyan 
pinfo = pblue
pdanger = pred
perr = pred


def notationScientifique(num, roundn=None, tuple=False):
    '''
    科学计数法 

    roundn : int, default None
        Notation Scientifique
        保留有效位数 
    tuple : bool, default False
        if True, return a tuple(head, pow) instead of string
    '''
    if num == 0:
        head, pow = 0,0
    else:
        loged = (math.log(abs(num),10))
        pow = int(loged) + (loged < 0 and -1)
        head = num*10**-pow
        if roundn is not None:
            head = round(head, roundn-1)
    if tuple:
        return (head, pow)
    s = '%se%d'%(str(head),pow)
    return s

def strnum(num, roundn=4):
    '''
    better str(num) avoid to long round
    support nan inf
    '''
    try:
        if isinstance(num, int):
            return str(num)
        elif not isinstance(num, float) and '__float__' in dir(num):
            num = float(num)
        head, pow = notationScientifique(num, roundn=roundn, tuple=True)
        if pow > roundn or pow < -min(3,roundn):
            s = '%se%d'%(str(head),pow)
        else:
            s = str(round(num, -pow+roundn))
        return s
    except (OverflowError, ValueError) as e:
        import numpy as np
        if np.isnan(num) or np.isinf(num):
            return str(num)
        raise e
def percentStr(num, roundn=2):
    '''
    float to percent sign
    roundn mean round to percent
    '''
    num = round(num*100, roundn)
    tabn = (2 if num <10 else 1 )if num <100 else 0
    return (' '*tabn+'%.'+str(roundn)+'f%%')%(num)
               
def ignoreWarning():
    from warnings import filterwarnings
    filterwarnings('ignore')


class LogLoopTime():
    '''
    记录循环信息的对象 主要的信息有每个循环时间和进度
    names: 用于循环的list，tuple
    digits: 时间的保留位数 可为负数
    loged: 是否直接打印
    
    使用时候 在循环最后加上 logLoopTime(name) 即可
    '''
    def __init__(self,names=None,digits=3,loged=True):
        self.ns = names
        self.begin = self.t = time.time()
        self.digits = digits
        self.loged = loged
        self.count = 0
    def __call__(self,name):
        digits = self.digits
        t = time.time()
        dt = t - self.t
        self.t = t
        times = ('%.'+str(digits)+'f')%dt if digits > 0 else '%.2fE%d'%(dt/10**abs(digits-1),abs(digits-1))
        if self.ns is None:
            s = 'No.%d  %s time:%s'%(self.count,name, times)
            self.count += 1
        else:
            names = self.ns
            ind = float(names.index(name))
            self.n = len(names)
            s = '%d/%d %.2f%%  %s time:%s'%(ind,self.n,
                                            (ind*100./self.n),name, times)
        if self.loged:
            log(s)
        return s
    log = __call__

class LogException():
    '''
    用于扑捉和记录函数中的异常错误
    usage:
        loge = LogException(logFilePath,otherFun) # 先实例一个对象
        loge.listen(f,*l,**args) # 用 .listen 运行函数
        @loge.decorator  # 装饰被监听函数
    '''
    def __init__(self,
                 logFilePath=None, 
                 otherFun=None,
                 printOnCmd=True, 
                 logBegin=False,
                 localTime=False,
                 isOn=True):
        '''logFilePath  log文件保存路径,为False时 不写入文件
        otherFun  一个返回字符串的函数，每次错误运行一次，结果写入log
        printOnCmd   时候在屏幕上打印
        logBegin     是否记录开始监听事件
        localTime    是否为当地时间 默认为GMT时间
        '''
        
        self.splitLine = '/*----------*/'
        self.path = logFilePath
        self.fun = otherFun if otherFun else lambda :''
        self.printt = printOnCmd
        self.localTime = localTime
        self.format = (
'''     Index :{index}, {time}
{timeClass} :{timeStr}
 Exception :{exceptionName}
   Message :{message}
      Args :{args}
{otherInfo}
{splitLine}
''')
        self.index = 0
        self.isOn = isOn
        if logFilePath:
            if os.path.isfile(logFilePath):
                with open(self.path,'r') as f:     
                    strr = f.read()
                self.index = strr.count(self.splitLine)
        if logBegin:
            class beginLogException(Exception):
                pass
            def f ():
                raise beginLogException('LogException is begin to log Exception!')
            self.listen(f)
        
    def listen(self,f,*l,**args):
        '''
        f        : 监听函数
        *l,**args: 函数f的参数
        '''
        import time
        if not self.isOn:
            f(*l,**args)
            return
        try:
            f(*l,**args)
        except Exception as e:
            exceptionName = tounicode(type(e))
            exceptionName = exceptionName[exceptionName.index('.')+1:-2]
            
            timeClass = 'Local time' if self.localTime else '  GMT time'
            t = time.asctime( time.localtime(time.time())) if self.localTime  else time.asctime(time.gmtime(time.time()))
            
            otherInfo = self.fun()
            
            erroStr = self.format.format(
                                         index=self.index,
                                         timeStr=t,
                                         timeClass=timeClass,
                                         time=time.time(),
                                         exceptionName=exceptionName,
                                         message=e.message,
                                         args=tounicode(e.args),
                                         otherInfo=otherInfo,
                                         splitLine=self.splitLine,
                                         )
            self.__writeLog(erroStr)
            self.index += 1
            self.last = self.e = e

    def __writeLog(self,strr):
        '''
        判断是否打印和写入
        '''
        if self.printt:
            print(strr)
        if self.path:
            with open(self.path,'a') as f:     
                f.write(strr)
    def decorator(self,f):
        '''
        函数装饰器封装
        '''
        def ff(*l,**arg):
            r = self.listen(f,*l,**arg)
            return r
        return ff

gsAttrDic = {}
class Gs(dict):
    '''debug的全局变量G的子类
    '''
    pass
    def __init__(self,name, log ,*l,**kv):
        idd = id(self)
        gsAttrDic[idd] = dicto()
        gsAttrDic[idd].log = log
        gsAttrDic[idd].name = name if name else 'g'
        dict.__init__(self,*l,**kv)
    def __setitem__(self, k, v):
        idd = id(self)
        if isinstance(v,tuple) and len(v) == 2 and (v[1] is self):
            v,tag = v
            if gsAttrDic[idd].log or (gsAttrDic[idd].log is None):
                pblue('%s[%s] ='%(gsAttrDic[idd].name, str(k)),v)
        else:
            if gsAttrDic[idd].log:
                pblue('%s[%s] ='%(gsAttrDic[idd].name, str(k)),v)
        dict.__setitem__(self, k, v)
        pass
    def logWhenSet(self, on='nothing'):
        idd = id(self)
        if on == 'nothing':
            gsAttrDic[idd].log = not gsAttrDic[idd].log
        else:
            gsAttrDic[idd].log = on
    def __call__(self, x=None):
        pretty = False
        if pretty:
            loc = prettyFrameLocation(1)
            pblue('Print by g from %s:'%loc)
        else:
            pblue('%s: %s'%(clf.p%'Print by g', x))
        return x
    __sub__ = __call__
    __lshift__ = __call__
    __rshift__ = __call__
    __truediv__ = __div__ = __call__
    
    def __del__(self):
        idd = id(self)
        if gsAttrDic and idd in gsAttrDic:
            del gsAttrDic[idd]
        
            
    

class SuperG(Gs):
    '''
    Author: DIYer22@GitHub (ylxx@live.com)
    **用于debug的全局变量**, 用了不少旁门左道以达到最低使用负担
    本身是类似JavaScript对象的超级字典，可以动态添加属性
    其中 g.keys,g.values,g.items 添加了property
    用法:
        1.获取变量
            g[0] = v 
            g.a = v
        2.在赋值时 同时打印
            g.a = v,g 
        3.始终在赋值时打印
            g.logWhenSet(True)
        4.替换print
            g(x)
            g<<x
            g-x
            g==x
        5.替换print 且返回本身
            g/x
    '''
    def __init__(self,name=None, log=None, *l, **kv):
        '''
        name: 变量名
        log: 时候打印 默认为None
            True: 都打印
            None: 跟着g才打印
            False: 都不打印
        '''
        Gs.__init__(self,name, log, *l, **kv)
    def __getattribute__(self, name=None, *l):
        if name in self:
            return self[name]
        if name in dir(Gs):
            return Gs.__getattribute__(self,name, *l)
        def keyError(x):
            self[name] = x
            return x
        return keyError
    def __setattr__(self, name, v):
        if name in dir(Gs):
            return Gs.__setattr__(self,name,v)
        self[name] = v
    if py2:
        @property
        def keys(self):
            return addCall(dict.keys(self))
        @property
        def values(self):
            return addCall(dict.values(self))
        @property
        def items(self):
            return addCall(dict.items(self))

sg = SuperG()


class withOperation():
    '''
    `w{operation}` is mulitple variables version of "{operation}/x", and work in "with statement".
    {usage}
    `w{operation}` only act on assignment variables that under `with w{operation}:` statement.
    
    Usage
    --------
        >>> with w{operation}:
        >>>     pi = 3.14
        >>>     e = 2.71
    
    Note
    --------
        If var's name in locals() and `id(var)` not change ,var may not be detected 
        Especially following cases：
            1. var is int and < 256
            2. `id(var)` not change

    '''
    def __init__(self, operation='p', printt=False, transport=False, deep=0):
        self.locs = defaultdict(lambda:[])
        self.operation = operation
        self.printt = printt
        self.transport = transport
        self.deep = deep
    def __enter__(self):
        f = sys._getframe(self.deep+1)
        ind = id(f)
        self.locs[ind].append((f.f_locals).copy())
        return self
    def __exit__(self, typee, value, traceback):
        f = sys._getframe(self.deep+1)
        ind = id(f)
        locsb = self.locs[ind].pop()
        locs = f.f_locals
        kvs = []
        newVars = []
        for k in locs:
            if k in locsb:
                if not (locsb[k] is locs[k]):
                    kvs.append((k, locs[k]))
            else:
                kvs.append((k, locs[k]))
                newVars.append(k)
        if self.transport:
            root = getRootFrame()
            root.f_locals.update(kvs)
        
        printf = lambda *l, **kv: 0
        if self.printt:
            printf = log
        printf("")
        printf(colorFormat.b%'withprint from %s'%prettyFrameLocation(f))

        if len(kvs):
            tag = ''
            if locs.get('__name__') == '__main__':
                printf(colorFormat.b% 'New Vars: ', end='')
                if len(newVars):
                    printf((', '.join([colorFormat.p%k for k in newVars])))
                else:
                    printf((colorFormat.b% 'None'))
                    
                tag = ("\nP.S. code run in __main__, some vars may not detected if id(var) not change.")
            printf((colorFormat.b% "All Vars's Values :"))#(P.S.some base object may not detected):"))
            if self.printt:
                from boxx import tree
                tree(dict(kvs))
                tag and printf(tag)
            
        else:
            print((colorFormat.r% '\n\nNot detected any Vars:'+
                   '\n    id(var) may not change in interactive mod if var is int and < 256 \n'+
                   '    `help(withprint)` for more infomation\n'+
                   '     P.S assignment self is not work for with statement.\n'+
                   '     Instead, `new_var = old_var` is OK!'))
    def __str__(self):
        s = self.__doc__
        if py2:
            return str(s.encode('utf-8'))
        return s
    __repr__ = __str__

class withPrint(withOperation):
    operation = 'p'
    usage = '''
    pretty print variables with their variable name.
    '''
    __doc__ = withOperation.__doc__.format(operation=operation, usage=usage)
    def __init__(self):
        withOperation.__init__(self, self.operation, True, False)
    
class withTransport(withOperation):
    operation = 'g'
    usage = '''
    `wg` will transport variable to Python interactive console.
    '''
    __doc__ = withOperation.__doc__.format(operation=operation, usage=usage)
    def __init__(self):
        withOperation.__init__(self, self.operation, False, True)

class withPrintAndTransport(withOperation):
    operation = 'gg'
    usage = '''
    `wgg` will transport variable to Python interactive console and pretty print they.
    '''
    __doc__ = withOperation.__doc__.format(operation=operation, usage=usage)
    def __init__(self):
        withOperation.__init__(self, self.operation, True, True)

wp = withPrint()
wg = withTransport()
wgg = withPrintAndTransport()

class TransportToRootFrame():
    def __init__(self, name=None, log=False):
        self.name = name
        self.log = log
    def __call__(self, value):
        frame = getRootFrame()
        frame.f_globals[self.name] = value
        if self.log:
            name = str(self.name)
            s = (clf.r%'gg.%s:"'+'%s'+clf.r%'"')%(name, tabstr(str(value), len(name)+5))
            print(s)
        return value
    __sub__ = __truediv__ = __div__ = __mul__ = __add__ = __eq__ = __pow__ = __call__
    def __str__(self):
        return 'TransportToRootFrame(name=%s, log=%s)'%(self.name, self.log)
    __repr__ = __str__
    
global_g_paras = {}
class GlobalGCore(object):
    def __init__(self, log=False):
        object.__init__(self)
        d = global_g_paras[id(self)] = dicto()
        d.log = log
        
        d.wo = withOperation(['g', 'gg'][log], printt=log, transport=True, deep=1)
    def __call__(self, deep=0):
        d = global_g_paras[id(self)]
        log = d.log
        out(depth=deep+1, printt=log)
    def __del__(self):
        idd = id(self)
        if global_g_paras and idd in global_g_paras:
            del global_g_paras[idd]

    def __enter__(self):
        d = global_g_paras[id(self)]
        return withOperation.__enter__(d.wo)
    def __exit__(self, typee, value, traceback):
        d = global_g_paras[id(self)]
        withOperation.__exit__(d.wo, typee, value, traceback)
class GlobalG(GlobalGCore):
    # TODO: add Decorators(装饰器) to catch error in with and export vars
    '''
    TODO:
        
    for dev-tips:
        after every operating in IPython@spyder, will read this instance 10+ times
        some times will read attr like "__xx__" but not in dir(object): in this case
        don't return anything just raise the Exception
        
        if is instance.__getattribute__(name) try to use getattr(instance, name) instead
    '''
    def __init__(self, log=False):
        GlobalGCore.__init__(self, log)
    def __getattribute__(self, name='x', *l):
#        print(id(self),name)
        if name.startswith('__') and name.endswith('__') or name in dir(GlobalGCore): 
            return GlobalGCore.__getattribute__(self, name, *l)
        log = global_g_paras[id(self)].log
        return TransportToRootFrame(name,log)
    def __setattr__(self, name, v):
        log = global_g_paras[id(self)].log
        transport = TransportToRootFrame(name,log)
        transport(v)
g = GlobalG()
gg = GlobalG(log=True)

config = dicto()
cf = config
boxxcf = dicto()

def if_main_then_g_call():
    '''`mg` is short of if_main_then_g_call
    Will transport `locals()` to Python interactive console when __name__ == '__main__'.
    Then return  __name__ == '__main__'
    
    >>> mg() 
    # equl to      
    >>> if __name__ == '__main__':
    >>>     g()
    '''
    frame = sys._getframe(1)
    _name_ = frame.f_globals['__name__']
    is_main = _name_ == '__main__'
    if is_main:
        g(1)
    return is_main
mg = if_main_then_g_call

def prettyClassFathers(obj):
    '''
    get object or type, return pretty str
    
    >>> prettyClassFathers(cf)
    Instance of boxx.tool.toolStructObj.dicto <-dict <-object
    '''
    fas = getfathers(obj)
    fas = [colorFormat.p%typeNameOf(fa) for fa in fas]
    s = 'Type' if istype(obj)  else 'Instance'
    s = colorFormat.r % s
    s += ' of '+ (' <-').join(fas)
    return s

def prettyFrameLocation(frame=0):
    '''
    get frame return pretty str
    
    >>> prettyFrameLocation(frame)
    "/home/dl/junk/printtAndRootFarme-2018.03.py", line 109, in wlf
    
    Parameters
    ----------
    frame : frame or int, default 0
        if int:相对于调用此函数frame的 int 深度的对应frame
    '''
    if isinstance(frame, int):
        frame = sys._getframe(1 + frame)
    c = frame.f_code
    return ((colorFormat.b%'File: "%s", line %s, in %s')%
            ('\x1b[32m%s\x1b[0m'% c.co_filename, '\x1b[32m%s\x1b[0m'% c.co_firstlineno, colorFormat.purple% c.co_name))

def getNameFromCodeObj(code, pretty=True):
    name = code.co_name
    filee = code.co_filename
    if pretty:
        if name == '<module>':
            if filee.startswith('<ipython-input-'):
                name = 'ipython-input'
            else:
                name = '%s'%os.path.basename(filee)
            name = '\x1b[36m%s\x1b[0m'%name
        if name == '<lambda>':
            return 'lambda'
    return name
def prettyFrameStack(frame=0, endByMain=True, maxprint=None):
    '''
    get frame return pretty str of stack
    
    >>> prettyFrameLocation(frame)
    __init__ <-f <-ff <-demo.py
    
    Parameters
    ----------
    frame : frame or int, default 0
        if int:相对于调用此函数frame的 int 深度的对应frame
    endByMain : bool, default True
        为 True 则在第一个 frame.f_locals[‘__name__’] == ‘__main__’ 处停止搜寻 
        目的是去除 IPython 自身多余的 Call Stack
    '''
    if frame is False and endByMain:
        frame, endByMain = 0, False
    if isinstance(frame, int):
        frame = sys._getframe(1 + frame)
    fs = getFatherFrames(frame, endByMain=endByMain)
    ns = [getNameFromCodeObj(f.f_code) for f in fs]
    if endByMain:
        if 'execfile' in ns:
            ns = ns[:ns.index('execfile')]
        if '_call_with_frames_removed' in ns:
            ns = ns[:ns.index('_call_with_frames_removed')]
    s = ' <-'.join(ns)
    s = shortStr(s, maxlen=maxprint)
    return s

def generaPAndLc():
    saveOut = {}
    class LocalAndGlobal(dicto):
        '''
        your can use `out()`, `p()` in any function or module
        exec `out()`, all vars that belong the function will transport to
        Python interactive shell. and `globals()` will in `p` which is a dicto
        
        BTW, `import boxx.out`, `import boxx.p` is Convenient way to use `out()` without `from boxx import out`
        
        在函数内运行`p()` or `lc()`  
        则此函数的global和local 变量会载入全局变量 p 中
        函数的 frame等其他信息 则放入全局变量 lc
        
        Parameters
        ----------
        depth : int or bool, default 0
            相对于`p()`所在frame的深度
            ps.为了使关闭printt简便 若`p(False)` 自动转换为`p(0, False)`
        printt : bool, default True
            是否打印
            
        Effect
        ----------
        out() : dicto
            copy current frame's locals() and globals() to your 
            Python interactive shell
            That's mean any var befor `out()` will Transport to Python shell,
            Even your are exec `out()` in Thearding
            ps. `out(False)` will turn off the info print
        p() : dicto
            将当前frame的locals()和globals()存入p
            p.var_name is the var's value in locals() and globals()
        lc : callabel dicto
            lc则存储更多、更细致的信息 包含code, frame, frames栈
            lc 的 items：
                self.c = self.code = frame.f_code
                self.l = self.local = locals()
                self.f = self.frame = frame
                self.fs = getFatherFrames(frame) 
        '''
        def __init__(self, out=False):
            saveOut[id(self)] = out
        def __call__(self, depth=0, printt=True):
            if depth is False:
                printt = depth
                depth = 0
            frame = sys._getframe(depth+1)
            code = frame.f_code
            p.clear()
            glob = frame.f_globals
            local = frame.f_locals
                
            self.c = self.code = code
            self.f = self.frame = frame
            self.l = self.local = local
            if printt:
                print('')
                prettyStr = prettyFrameLocation(frame)
                print(prettyStr)
                fs = getFatherFrames(frame)
                self.fs = fs
                s = prettyFrameStack(frame)
                print((colorFormat.b%'Stacks: '+colorFormat.r%s))
                print((colorFormat.b%'Locals: '))
                from boxx import tree
                tree(local, maxprint=100)
                
            if saveOut[id(self)]:
                p.update(glob)
                p.update(local)
                root = getRootFrame()
                addDic = dict(
#                        code=code,
#                        frame=frame,
#                        local=local,
#                        glob=glob,
#                        gl=glob,
#                        rootGlob=root.f_globals,
                        )
                
                
                addDic.update(local)
                same = set(addDic).intersection(set(root.f_globals))
                
                if printt:
                    print("")
                    addVarStr = ', '.join([colorFormat.p%k for k in addDic if k not in same])
                    if addVarStr:
                        print(colorFormat.b% '\nVars add to Console Frame: '+'\n└── '+ addVarStr)
                    if len(same):
                        print(colorFormat.r% '\nVars that replaced in Console Frame: '+'\n└── '+', '.join([colorFormat.p%k for k in same]))
                root.f_globals.update(addDic)
                lc.c = lc.code = code
                lc.f = lc.frame = frame
                lc.l = lc.local = local
                self.clear()
                self.update(local)
    
    
    __P_CACHE__ = dicto()
    class Pdicto(dicto):
        '''
        # print(x) and return x
        >>> p/517 
        517
        517
        
        # p() to pretty print all variables in function with thier name
        >>> def f(arg=517):
                l = [1, 2]
                p()
        
            ├── l: list  2
            │   ├── 0: 1
            │   └── 1: 2
            └── arg: 517
        import boxx.p has same usage
        
        # p will pretty print mulit variables under "with statement"
        
        >>> with p:
            
        '''
        def __call__(self, depth=0, printt=True):
            if depth is False:
                printt = depth
                depth = 0
            lc(depth+1, printt)
        def printt(self, x=None):
            pretty = False
#            root = getRootFrame()
#            root.f_globals['pp'] = x
            if pretty:
                loc = prettyFrameLocation(1)
                pblue('Print by p from %s:'%loc)
            else:
                pass
#                pblue('%s: %s'%(clf.p%'As pp by p', x))
                print(x)
            return x
        __sub__ = printt
        __lshift__ = printt
        __rshift__ = printt
        __truediv__ = __div__ = printt
        __pow__ = printt
        
        def __enter__(self):
            d = __P_CACHE__
            if 'wo' not in d:
                d.wo = withOperation('p', printt=True, transport=False, deep=1)
            return withOperation.__enter__(d.wo)
        def __exit__(self, typee, value, traceback):
            d = __P_CACHE__
            withOperation.__exit__(d.wo, typee, value, traceback)
    p = Pdicto()
    lc = LocalAndGlobal()
    out = LocalAndGlobal(out = True)
    return p, lc, out
p, lc, out = generaPAndLc()
pp = "registered `pp` var name that will be used by `p/x`"
#pp, lcc, outt = generaPAndLc()

