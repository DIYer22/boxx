#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 21:27:28 2018

@author: yanglei
"""

import sys, os
from os import environ


class SystemInfo():
    '''
    sys info
    '''
    os = sys.platform
    # to do
    gui = True
    
    display = 'DISPLAY' in environ and environ['DISPLAY']
    
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

def getIPytonConfig():
    try:
        cfg = get_ipython().config
        return cfg
    # to do 
        if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
            return 'jn'
        else:
            return 'qt'
    except (NameError,KeyError):
        return None

class pyi():
    config = getIPytonConfig()
    
    cmdipython = 'IPython' in sys.modules
    gui = 'ipykernel' in sys.modules

    ipython = cmdipython or gui
    cmd = not ipython
    
    # to do
    qt = jn = gui
pyv = sys.version_info.major
py3 = (pyv == 3)
py2 = (pyv == 2)

linuxYl = sysi.os.startswith('linux')
windowsYl = sysi.os.startswith('win')

import multiprocessing as __module
cpun = __module.cpu_count()

cloud = cpun > 16

if linuxYl:
    cuda = not os.system('nvcc --version> /dev/null 2>&1')
else:
    cuda = 'Not Implemented'
usecuda = 'auto' # auto: auto, False: not use
    
if linuxYl:
    homeYl = os.getenv('HOME') + '/'
    tmpYl = '/tmp/'
elif windowsYl:
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


