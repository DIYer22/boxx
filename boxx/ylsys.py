#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
A module provide system info and Python Info for boxx

@author: yanglei
"""

import sys, os
from os import environ

def jupyterNotebookOrQtConsole():
    env = 'Unknow'
    cmd = 'ps -ef'
    try:
        with os.popen(cmd) as stream:
            if not py2:
                stream = stream._stream
            s = stream.read()
        pid = os.getpid()
        ls = list(filter(lambda l:'jupyter' in l and str(pid) in l.split(' '), s.split('\n')))
        if len(ls) == 1:
            l = ls[0]
            import re
            pa = re.compile(r'kernel-([-a-z0-9]*)\.json')
            rs = pa.findall(l)
            if len(rs):
                r = rs[0]
                if len(r)<12:
                    env = 'qtipython'
                else :
                    env = 'jn'
        return env
    except:
        return env
    print(r, env)

pyv = sys.version_info.major
py3 = (pyv == 3)
py2 = (pyv == 2)


linuxYl = sys.platform.startswith('linux')
winYl = sys.platform.startswith('win')
osxYl = sys.platform.startswith('darwin')

import multiprocessing as __module
cpun = __module.cpu_count()

cloud = cpun > 8

if linuxYl or osxYl:
    cuda = not os.system('nvidia-smi> /dev/null 2>&1')
elif winYl:
    import subprocess
    try:
        cuda = not subprocess.call('nvidia-smi', creationflags=0x00000008)
    except FileNotFoundError:
        cuda = False
usecuda = 'auto' # auto: auto, False: not use
    
if linuxYl or osxYl:
    homeYl = os.getenv('HOME') + '/'
    tmpYl = '/tmp/'
elif winYl:
    homeYl = os.path.expanduser("~")
    tmpYl = os.getenv('TMP') + '\\'

class __TmpboxxWithCall(str):
    '''
    the tmp dir for boxx 
    use tmpboxx() to get tmpdir 
    use tmpboxx({dirname}) to get tmpdir/{dirname}
    if not exist then will auto mkdir of boxxTmp in `/tmp`
    '''
    def __call__(self, dirName=None):
        dirr = os.path.join(self, dirName) if dirName else self
        
        if not os.path.isdir(dirr):
            os.makedirs(dirr, exist_ok=True)
        return dirr
tmpboxx = __TmpboxxWithCall(os.path.join(tmpYl,'boxxTmp/'))

class PythonInfo():
    '''
    python info
    
    plt : Bool
        mean plt avaliable
    env :
        belong [cmd, cmdipython, qtipython, spyder, jn]
    '''
    pid = os.getpid()
    gui = 'ipykernel' in sys.modules
    cmdipython = 'IPython' in sys.modules and not gui
    ipython = cmdipython or gui
    spyder = 'spyder' in sys.modules
    if gui:
        env = 'spyder' if spyder else jupyterNotebookOrQtConsole()
    else:
        env = 'cmdipython' if ipython else 'cmd'
    
    cmd = not ipython
    qtipython = env == 'qtipython'
    jn = env == 'jn'
    
    interactive = bool(getattr(sys, 'ps1', sys.flags.interactive))
    
    plt = True
    if not gui and linuxYl and 'DISPLAY' not in os.environ :
        plt =  False
    reloadplt = False
    def __str__(self):
        from boxx import strMethodForDiraAttrs
        return strMethodForDiraAttrs(self)
    __repr__ = __str__
pyi = PythonInfo()

class SystemInfo():
    '''
    sys info
    '''
    pyv = pyv
    cpun = cpun
    cuda = cuda
    tmp = tmpYl
    
    linux = linuxYl
    win = winYl
    osx = osxYl
    
    os = sys.platform
    display = True
    if linuxYl:
        display = 'DISPLAY' in environ and environ['DISPLAY']
        from os.path import expanduser
        home = expanduser('~')
    gui = pyi.gui or display
    
    @staticmethod
    def ip_by_target_ip(target_ip="8.8.8.8"):
        import socket
    
        return [
            (s.connect((target_ip, 80)), s.getsockname()[0], s.close())
            for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
        ][0][1]

    @property
    def ip(self):
        return self.ip_by_target_ip()

    @property
    def user(self):
        try:
            import getpass
            return getpass.getuser()
        except KeyError:
            return "unknow"
            
    @property
    def host(self):
        import platform
        return platform.node()
    def __str__(self):
        attrs = {k:str(getattr(self, k)) for k in dir(self) 
                 if not k.startswith('__') and not callable(getattr(self, k))}
        return "\n".join(map(lambda items:"\t%s: %s"%items, attrs.items()))
    __repr__ = __str__
sysi = SystemInfo()
