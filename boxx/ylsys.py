#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 21:27:28 2018

@author: yanglei
"""

import sys, os



class SystemInfo():
    '''
    sys info
    '''
    os = sys.platform
    # todo
    qt = True
    ipython = True
    gui = True
    
    
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


import multiprocessing as __module
cpun = __module.cpu_count()

pyv = sys.version_info.major
py3 = (pyv == 3)
py2 = (pyv == 2)

cloud = cpun > 16

linuxYl = sysi.os.startswith('linux')
windowsYl = sysi.os.startswith('win')

if linuxYl:
    homeYl = os.getenv('HOME') + '/'
    tmpYl = '/tmp/'
else:
    homeYl = ''
    tmpYl = ''
    