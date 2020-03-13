#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Mon Mar  2 12:52:18 2020

Make python script as easy to use as shell script.

Usage:
    python -m boxx.script '[print(i) for i in range(10)]'
    
    # add "tmp_" as prefix for all file in '.' 
    python -m boxx.script '[mv(fname, "tmp_"+fname) for fname in ls()]'

alias "ls, mv, ln, lns, cp, cpr" as funcation.

"""

from boxx import *
from boxx import listdir

try:
    import cv2
    #from boxx.ylth import *
except Exception:
    pass

import sys
import shutil
from os import rename, link, symlink, remove

mv = rename
rm = remove
ln = link
lns = symlink
cp = shutil.copy
cpr = shutil.copytree
ls = listdir


class GetKey(dict):
    def __getitem__(self, k):
        if k in self:
            return dict.__getitem__(self, k)
        elif k in __builtins__.__dict__:
            return __builtins__.__dict__[k]
        else:
            print('Set %s as string:"%s"' % (k, k))
            self[k] = k
            return dict.__getitem__(self, k)


context = GetKey(globals())

def main():
    code = " ".join(sys.argv[1:])
    print('Code: "%s"' % code)
    print()

    exec(code, context, context)

if __name__ == "__main__":
    main()