# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os,sys,time
from toolStructObj import addCall,dicto,FunAddMagicMethod

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
    fun : funcation, default None
        每一次要执行fun()
        
    Attribute
    ----------
    __call__ : 
        返还 当前轮数(True)
    time : @property
        is @property 返回已记录的时长
    '''
    def __init__(self, gap=1,fun=False):
        self.n = 0
        self.gap = gap
        self.begin = self.last = time.time()
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
        return map(lambda c:stdout((c+' '*10)[:7]) and pcolor(c,": "+str(s)), frontColorDic) and None
    pall = printAllColor
    
def tounicode(strr):
    '''
    Python 中文编码错误解决方案，用于代替str类及函数, 全部换成unicode
    '''
    if isinstance(strr,unicode):
        return strr
    strr = str(strr)
    if isinstance(strr,str):
        return strr.decode('utf-8','replace')
    return unicode(strr)


def pcolor(color, *s):
    '''
    用颜色打印 不返回
    '''
    if not isinstance(color,int):
        color = frontColorDic[color]
    print('\x1b[%dm%s\x1b[0m'%(color, ' '.join(map(tounicode,s))))
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

def log(*l,**dic):
    if len(l) == 1:
        pblue(l[0])
    else:
        pblue('\n'.join(map(tounicode,l)))
    if len(dic):
        for k in dic:
            pblue('%s = %s'%(k,tounicode(dic[k])))
    if len(l) == 1:
        return l[0]
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
    __sub__ = __lshift__ = __rshift__  = __div__ = __call__
    def __repr__(self):
        blue  = '\x1b[%dm%s\x1b[0m'%(frontColorDic['red'],tounicode(len(self) and self[len(self)-1]))
        return '''LogAndSaveToList(printFun=%s, cache=%s) log[-1]: %s'''%(
        str(self.p),self.cache,blue)
    __str__ = __repr__

logg = LogAndSaveToList()
pcyan,pred,ppurple,stdout = map(FunAddMagicMethod,
                                        [pcyan,pred,ppurple,stdout])
    
pblue = pcyan 
pinfo = pblue
pdanger = pred
perr = pred

               
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
                raise beginLogException,'LogException is begin to log Exception!'
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
            print strr
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
        pblue(x)
        return x
    __sub__ = __call__
    __lshift__ = __call__
    __rshift__ = __call__
    __div__ = __call__
        
    
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
    @property
    def keys(self):
        return addCall(dict.keys(self))
    @property
    def values(self):
        return addCall(dict.values(self))
    @property
    def items(self):
        return addCall(dict.items(self))

GlobalG = SuperG
g = SuperG()
config = dicto()
cf = config



class LocalAndGlobal(dicto):
    '''
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
    p : dicto
        将当前frame的locals()和globals()存入p
        运行 `p()`, 等价于 p.update(globals());p.update(locals())
    lc : callabel dicto
        lc则存储更多、更细致的信息 包含code, frame, frames栈
        lc 的 items：
            self.c = self.code = frame.f_code
            self.l = self.local = locals()
            self.f = self.frame = frame
            self.fs = __getFatherFrames__(frame) 
    '''
    def __call__(self, depth=0, printt=True):
        if depth is False:
            printt = depth
            depth = 0
        frame = sys._getframe(depth+1)
        code = frame.f_code
        p.clear()
        glob = frame.f_globals
        local = frame.f_locals
        p.update(glob)
        p.update(local)
        self.c = self.code = code
        self.f = self.frame = frame
        self.l = self.local = local
        if printt:
            print('')
            c = code
            print((colorFormat.b%'File: "%s", line %s, in %s')%(u'\x1b[32m%s\x1b[0m'% c.co_filename, u'\x1b[32m%s\x1b[0m'% c.co_firstlineno, colorFormat.purple% c.co_name))
            fs = __getFatherFrames__(frame)
            self.fs = fs
            ns = map(lambda f:__getNameFromCodeObj__(f.f_code), fs)
            if 'execfile' in ns:
                ns = ns[:ns.index('execfile')]
            MAX_PRINT_LEN = 100
            s = ' <-'.join(ns)
            s = s if len(s) <= MAX_PRINT_LEN else (s[:MAX_PRINT_LEN-3]+'...')
            print(colorFormat.b%'Stacks: '+colorFormat.r%s)
            print(colorFormat.b%'Locals: ')
            from boxx import tree
            tree(local, 1)
def __getFatherFrames__(frame):
    fs = []
    while frame:
        fs.append(frame)
        frame = frame.f_back
    return fs

def __getNameFromCodeObj__(code):
    name = code.co_name
    filee = code.co_filename
    
    if name == '<module>':
        if filee.startswith('<ipython-input-'):
            name = 'ipython-input'
        else:
            name = '%s'%os.path.basename(filee)
        name = u'\x1b[36m%s\x1b[0m'%name
    if name == '<lambda>':
        return 'lambda'
    return name

class __P__(dicto):
    def __call__(self, depth=0, printt=True):
        if depth is False:
            printt = depth
            depth = 0
        lc(depth+1, printt)
p = __P__()
lc = LocalAndGlobal()

if __name__ == "__main__":
    colorFormat.pall()
    pass