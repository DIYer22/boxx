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


rad2deg = lambda rad:rad/pi*180
deg2rad = lambda deg:deg/180*pi

def degShift(trifun, inpIsAngle=True):
    @wraps(trifun)
    def innerfun(inp):
        if inpIsAngle:
            inp = deg2rad(inp)
        r = trifun(inp)
        if not inpIsAngle:
            r = rad2deg(r)
        return r
    return innerfun
sin = degShift(np.sin)
cos = degShift(np.cos)

arctan = degShift(np.arctan,  False)
arccos = degShift(np.arccos,  False)

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
    
    @x.setter
    def x(self, v, *l):
        self[0] = v
    @y.setter
    def y(self, v, *l):
        self[1] = v
    
    def intround(self):
        return self.round().astype(int)
        
    @property
    def norm(self):
        if self._norm is None:
            self._norm = (np.array(self)**2).sum()**.5
        return self._norm
    
    def angleWith(self, v):
        cosin = (self * v).sum()/(self.norm*v.norm)
        deg = arccos(cosin)
        return deg
    def rotation(self, deg):
        transferMatrix = [[cos(deg), -sin(deg)],[sin(deg), cos(deg)]]
        after = np.dot(transferMatrix, self.T).T
        return Vector(after)
    def __str__(self, ):
        if (self).shape == (2,):
            return "V(x=%s, y=%s)%s"%(strnum(self[0]), strnum(self[1]), self.dtype)
        return np.ndarray.__str__(self,) + ' (Vector)'
    __repr__ = __str__
    
    @staticmethod
    def test():
        a = Vector([4, 0])
        b = Vector([4, 4*3**.5])
        print(a.angleWith(b))
        print(a.rotation(45).norm)
    


if __name__ == "__main__":
    Vector.test()
    pass
    
    
