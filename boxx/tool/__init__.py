# -*- coding: utf-8 -*-
"""
General Python Tools for Debugging, Logging, Magic .etc

@author: yanglei
"""

from __future__ import unicode_literals

import os, sys, time
from ..ylsys import py2

from .toolLog import (stdout, log, logc, printt, PrintStrCollect, printToStr, logg, tounicode, tostrpy2,
                      shortDiscrib, shortStr, discrib, getDoc, tabstr, ignoreWarning, LogException, 
                      LogLoopTime, SuperG, sg, g, gg, cf, p, pp, lc, out)
from .toolLog import colorFormat, clf, pblue, pred, pdanger, perr, pinfo, decolor
from .toolLog import strnum, percentStr, notationScientifique
from .toolLog import prettyClassFathers, prettyFrameLocation, prettyFrameStack, wp, wg, wgg
from .toolLog import localTimeStr, gmtTimeStr, timeGap, timegap

from .toolStructObj import (dicToObj, dicto, typeNameOf, typestr, strMethodForDiraAttrs, 
                            getfathers, getfather, generator,
                            nextiter, listToBatch, sliceInt, ll, FunAddMagicMethod, mf, addCall,
                            setself, unfoldself, withfun, withattr, isinstancestr)

from .toolIo import (getsize, getsizem, listdir, filename, openread, openwrite, replaceTabInPy, saveData, 
                    loadData, fileJoinPath,  warn, warn1time, BoxxException, BoxxWarning, OffScreenWarning,
                    Except, excep, getExcept, browserOpen)
save_data = saveData
load_data = loadData

from .toolSystem import (crun, performance, timeit, heatmap, getArgvDic, softInPath, execmd, addPathToSys)
from .toolSystem import importAllFunCode, impt, tryImport, FakeModule, removeImportSelf,  removeimp
from .toolSystem import getMainFrame, getRootFrame, getFatherFrames#, exceptionHook

from .toolFunction import (getFunName, dynamicWraps, setTimeOut, pipe,
                           setInterval, multiThread, mapmp, mapmt, retry)

from .toolTools import (intround, increase, filterList, findints, randint, randfloat, randchoice,
                       listdirWithFun, replaceAllInRoot, findinRoot)

from glob import glob
from os.path import join as pathjoin
from os.path import basename, isfile, isdir, dirname

from collections import namedtuple, defaultdict, Counter, OrderedDict
dictd = defaultdict
odict = OrderedDict

from time import sleep
from functools import reduce, wraps
from operator import add, sub, mul
if py2:
    from operator import div
else :
    from operator import truediv as div
from fn import _ as x_
x = x_

from functools import wraps


if __name__ == "__main__":
    pass