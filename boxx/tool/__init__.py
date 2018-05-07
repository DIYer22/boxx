# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os, sys, time
from ..ylsys import py2

from .toolLog import (stdout, log, logc, printt, logg, tounicode,
                      shortstr, shortDiscrib, discrib, getDoc, tabstr, ignoreWarning, LogException, 
                      LogLoopTime, SuperG, g, cf, p, lc, out)
from .toolLog import colorFormat, clf, pblue, pred, pdanger, perr, pinfo, decolor
from .toolLog import strnum, percentStr, notationScientifique
from .toolLog import prettyClassFathers, prettyFrameLocation, prettyFrameStack, withprint, wp
from .toolLog import localTimeStr, gmtTimeStr, timeGap, timegap

from .toolStructObj import (dicToObj, dicto, typeNameOf, typestr, getfathers, getfather,
                            nextiter, listToBatch, ll, FunAddMagicMethod)

from .toolIo import (getsize, getsizem, listdir, filename, openread, openwrite, replaceTabInPy, saveData, 
                    loadData, fileJoinPath, BoxxException)
save_data = saveData
load_data = loadData

from .toolSystem import (importAllFunCode, impt, tryImport, FakeModule, removeImportSelf,  crun, frun, 
                        timeit, heatMap, getArgvDic, softInPath, addPathToSys)
from .toolSystem import getRootFrame, getFatherFrames#, exceptionHook

from .toolFuncation import (getFunName, dynamicWraps, setTimeOut, pipe,
                           setInterval, multiThread, mapmp, mapmt, retry)

from .toolTools import (increase, filterList, findints, randint, randfloat, randchoice,
                       listdirWithFun, replaceAllInRoot, findinRoot)

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

from functools import wraps


if __name__ == "__main__":
    pass