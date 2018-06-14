#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 21:27:28 2018

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

cloud = cpun > 16

if linuxYl or osxYl:
    cuda = not os.system('nvcc --version> /dev/null 2>&1')
else:
    cuda = 'Not Implemented'
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
    if not exist then will auto mkdir of boxxTmp in `/tmp`
    '''
    def __call__(self):
        if not os.path.isdir(self):
            os.makedirs(self)
        return self
tmpboxx = __TmpboxxWithCall(os.path.join(tmpYl,'boxxTmp/'))

class pyi():
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
class SystemInfo():
    '''
    sys info
    '''
    linux = linuxYl
    win = winYl
    osx = osxYl
    
    os = sys.platform
    display = True
    if linuxYl:
        display = 'DISPLAY' in environ and environ['DISPLAY']
    gui = pyi.gui or display
    
    @property
    def ip(self):
        return '127.0.0.1'
    @property
    def user(self):
        import getpass
        return getpass.getuser()
    @property
    def host(self):
        import platform
        return platform.node()
sysi = SystemInfo()
