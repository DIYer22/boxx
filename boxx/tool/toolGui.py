#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Fri Jun 21 13:38:11 2019
"""
from __future__ import unicode_literals
import os

from .toolStructObj import FunAddMagicMethod

def startGnomeTerminal(dirr=None):
    from ..ylsys import linuxYl
    assert linuxYl
    if dirr is None:
        os.system('gnome-terminal ')
    elif os.path.isfile(dirr):
        os.system('gnome-terminal  --working-directory "%s"'%os.path.abspath(os.path.dirname(dirr)))
    else:
        os.system('gnome-terminal  --working-directory "%s"'%os.path.abspath(dirr))
        
ter = FunAddMagicMethod(startGnomeTerminal)


def startNautilus(dirr=None):
    from ..ylsys import linuxYl
    assert linuxYl
    if dirr is None:
        os.system('nautilus .')
    elif os.path.isfile(dirr):
        os.system('nautilus "%s"'%os.path.dirname(dirr))
    else:
        os.system('nautilus "%s"'%dirr)
nau = FunAddMagicMethod(startNautilus)


def startVscode(dirr=None, relpath=None):
    if dirr is None:
        dirr = '.'
    dirr = os.path.abspath(dirr)
    if relpath is not None:
        dirr = os.path.abspath(os.path.join(dirr, relpath))
    os.system('code "%s"' % dirr)
    
vscode = startVscode

if __name__ == "__main__":
    pass
    
    
    
