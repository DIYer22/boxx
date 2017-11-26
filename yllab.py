# -*- coding: utf-8 -*-
import sys
from os.path import abspath,join,dirname
_path = (abspath(__file__))
absLibpPath = join(dirname(_path),'yl')
    
if absLibpPath not in sys.path:
    sys.path = [absLibpPath]+sys.path
# print absLibpPath
from yl.tool import *
from yl.ylimg import *
from yl.ylml import * 
from yl.ylnp import *
from yl import tool
from yl import ylimg
from yl import ylml
from yl import ylnp


if __name__ == '__main__':

    pass
