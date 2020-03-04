#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Mon Mar  2 12:52:18 2020
"""

from boxx import *

try:
    import cv2
    from boxx.ylth import *
except Exception:
    pass

import sys


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

if __name__ == "__main__":
    code = " ".join(sys.argv[1:])
    # print("Input:", sys.argv[1:])
    print('Code: "%s"' % code)
    print()

    exec(code, context, context)
