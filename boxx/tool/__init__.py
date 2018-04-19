# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os, sys, time
from ..ylsys import py2

from .toolLog import (stdout, log, tounicode, ignoreWarning, LogException, 
                     LogLoopTime, SuperG, g, cf, p, lc)
from .toolLog import colorFormat, pblue, pred, pdanger, perr, pinfo
from .toolLog import localTimeStr, gmtTimeStr, timeGap

from .toolStructObj import (dicToObj, dicto, typeNameOf, typestr,
                                        listToBatch, FunAddMagicMethod)

from .toolIo import (listdir, filename, openread, openwrite, replaceTabInPy, save_data, 
                    load_data, fileJoinPath)

from .toolSystem import (importAllFunCode, impt, tryImport, FakeModule, crun, frun, 
                        timeit, heatMap, getArgvDic, softInPath, addPathToSys)

from .toolFuncation import (getFunName, dynamicWraps, setTimeOut, pipe,
                           setInterval, multiThread, mapmp, mapmt, retry)

from .toolTools import (filterList, findints, randint, randfloat, randchoice,
                       listdirWithFun, replaceAllInRoot)

from glob import glob
from collections import namedtuple, defaultdict, Counter
dictd = defaultdict
from functools import reduce
from os.path import join as pathjoin
from os.path import basename, isfile, isdir, dirname
from operator import add, sub, mul
if py2:
    from operator import div
else :
    from operator import truediv as div
if __name__ == "__main__":
    pass