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
import boxx
from boxx import *
from os import *
from os.path import *


_tmp_list_as_None = []
class DictCouldSetAttr(dict):
    def __setattr__(self, name, value):
        self[name] = value
        return value

    set = __setattr__
    
    def __getattr__(self, name):
        if name in self:
            return self[name]
        return super().__getattribute__(name)
    
    def __call__(self, value=_tmp_list_as_None):
        """Store one tmp var by call
        >>> print(tmp('tmp_value1'), tmp(), tmp('tmp_value2'), tmp())
        tmp_value1 tmp_value1 tmp_value2 tmp_value2
        """
        if value is _tmp_list_as_None:
            if not len(_tmp_list_as_None):
                raise ValueError("Please register tmp value by `tmp(value)` first!")
            return _tmp_list_as_None[-1]
        else:
            _tmp_list_as_None.clear()
            _tmp_list_as_None.append(value)
            return value

d = tmp = DictCouldSetAttr()


import os
import sys
import shutil
from os import rename, link, symlink, remove

mv = rename
rm = remove
ln = link
lns = symlink
copy = shutil.copy
copytree = shutil.copytree

def sh(cmd):
    return boxx.execmd(cmd).strip().split()
bash = sh

def ls(path=".", a=False):
    cmd = 'ls "' + path + '"' + (' -a ' if a else '')
    return sh(cmd)

def cp(src, dst):
    cmd = 'cp -r "' if os.path.isdir(src) else 'cp "'
    cmd += src + '" "' + dst + '"'
    return sh(cmd)

cpr = cp


def cat(*paths):
    for path in paths:
        if len(paths) > 1:
            print("-"*5, path, "-"*5)
        with open(path, 'r') as f:
            print(f.read())

builtins_dict = __builtins__ if isinstance(__builtins__, dict) else __builtins__.__dict__
class GetKey(dict):
    def __getitem__(self, k):
        if k in self:
            return dict.__getitem__(self, k)
        elif k in builtins_dict:
            return builtins_dict[k]
        else:
            try:
                print('try import %s' % (k,))
                self[k] = __import__(k)
            except ModuleNotFoundError as e:
                if e.name != k:
                    raise e
            return dict.__getitem__(self, k)


context = GetKey(globals())

def main():
    if len(sys.argv) <= 1:
        __file__ = os.path.abspath('temp.py')

        import IPython

        IPython.embed()
    else:
        code = " ".join(sys.argv[1:])
        print('Code: "%s"' % code)
        print()
    
        exec(code, context, context)

if __name__ == "__main__":
    main()