# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from os.path import abspath,join,dirname

yllibPath = abspath(join(dirname(abspath(__file__)),'.'))
if yllibPath not in sys.path:
    sys.path = [yllibPath] + sys.path
    
import tool
import yldb
import py3
import undetermined
import ylimg
import ylnp
import ylml
if __name__ == '__main__':
    print (yldb, py3, tool, ylimg, ylnp)
    tool.importAllFunCode('yl')
    pass

