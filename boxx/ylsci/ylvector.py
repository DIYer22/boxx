# -*- coding: utf-8 -*-
"""
Vector Class

Note:
    we use deg rather than rad, for human

@author: yl
"""
from functools import wraps

import numpy as np
from numpy import pi

from ..tool import strnum
from ..ylcompat import py2

rad2deg = lambda rad: rad / pi * 180
deg2rad = lambda deg: deg / 180 * pi

# TODO mv to ylTriFun.py
def degShift(triFun, arc=False):
    funForInfo = lambda: 0 if py2 else triFun
    @wraps(funForInfo)
    def innerfun(inp):
        if not arc:
            inp = deg2rad(inp)
        r = triFun(inp)
        if arc:
            r = rad2deg(r)
        return r
    return innerfun

sin = degShift(np.sin)
cos = degShift(np.cos)
tan = degShift(np.tan)

arcsin = degShift(np.arcsin, arc=True)
arccos = degShift(np.arccos, arc=True)
arctan = degShift(np.arctan, arc=True)


class Vector(np.ndarray):
    #    def __init__(self, point):
    #        np.ndarray.__init__(self, point)
    #        self._norm = None
    def __new__(self, point):
        obj = np.asarray(point).view(self)
        self._norm = None
        return obj

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @x.setter
    def x(self, v, *l):
        self[0] = v

    @y.setter
    def y(self, v, *l):
        self[1] = v

    @z.setter
    def z(self, v, *l):
        self[2] = v

    @property
    def h(self):
        return self[0]

    @property
    def w(self):
        return self[1]

    @h.setter
    def h(self, v, *l):
        self[0] = v

    @w.setter
    def w(self, v, *l):
        self[1] = v

    def intround(self):
        return self.round().astype(int)

    @property
    def norm(self):
        if self._norm is None:
            self._norm = (np.array(self) ** 2).sum() ** 0.5
        return self._norm

    def angleWith(self, v):
        cosin = (self * v).sum() / (self.norm * v.norm)
        deg = arccos(cosin)
        return deg

    def rotation(self, deg):
        assert self.shape == (2,)
        transferMatrix = [[cos(deg), -sin(deg)], [sin(deg), cos(deg)]]
        after = np.dot(transferMatrix, self.T).T
        return Vector(after)

    def __str__(self,):
        if (self).shape == (2,):
            if "int" in str(self.dtype):
                return "Vector(x|h=%s, y|w=%s)%s" % ((self[0]), (self[1]), self.dtype)
            return "Vector(x|h=%s, y|w=%s)%s" % (
                strnum(self[0]),
                strnum(self[1]),
                self.dtype,
            )
        if (self).shape == (3,):
            if "int" in str(self.dtype):
                return "Vector(x|h=%s, y|w=%s, z=%s)%s" % (
                    (self[0]),
                    (self[1]),
                    (self[2]),
                    self.dtype,
                )
            return "Vector(x|h=%s, y|w=%s, z=%s)%s" % (
                strnum(self[0]),
                strnum(self[1]),
                strnum(self[2]),
                self.dtype,
            )
        return np.ndarray.__str__(self) + " (Vector)"

    __repr__ = __str__

    @staticmethod
    def test():
        a = Vector([4, 0])
        b = Vector([4, 4 * 3 ** 0.5])
        print(a.angleWith(b))
        print(a.rotation(45).norm)


v0 = Vector([0, 0])

if __name__ == "__main__":
    Vector.test()
    pass
