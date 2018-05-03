# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os, sys, time
from ..ylsys import py2

from .toolLog import (stdout, log, printt, logg, tounicode,
                      shortDiscrib, discrib, getDoc, tabstr, ignoreWarning, LogException, 
                     LogLoopTime, SuperG, g, cf, p, lc, out)
from .toolLog import colorFormat, clf, pblue, pred, pdanger, perr, pinfo
from .toolLog import prettyClassFathers, prettyFrameLocation, prettyFrameStack, withprint, wp
from .toolLog import localTimeStr, gmtTimeStr, timeGap

from .toolStructObj import (dicToObj, dicto, typeNameOf, typestr, getfathers, getfather,
                            nextiter, listToBatch, FunAddMagicMethod)

from .toolIo import (getsize, getsizem, listdir, filename, openread, openwrite, replaceTabInPy, saveData, 
                    loadData, fileJoinPath)
save_data = saveData
load_data = loadData

from .toolSystem import (importAllFunCode, impt, tryImport, FakeModule, crun, frun, 
                        timeit, heatMap, getArgvDic, softInPath, addPathToSys)
from .toolSystem import getRootFrame, getFatherFrames#, exceptionHook

from .toolFuncation import (getFunName, dynamicWraps, setTimeOut, pipe,
                           setInterval, multiThread, mapmp, mapmt, retry)

from .toolTools import (increase, filterList, findints, randint, randfloat, randchoice,
                       listdirWithFun, replaceAllInRoot, findInRoot)

from glob import glob
from os.path import join as pathjoin
from os.path import basename, isfile, isdir, dirname

from collections import namedtuple, defaultdict, Counter, OrderedDict
dictd = defaultdict
odict = OrderedDict

from time import sleep
from functools import reduce
from operator import add, sub, mul
if py2:
    from operator import div
else :
    from operator import truediv as div
from fn import _ as x_
x = x_


if __name__ == "__main__":
    pass