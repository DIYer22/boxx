# -*- coding: utf-8 -*-
"""
Math and Scientific Computing module

@author: yl
"""

from __future__ import unicode_literals

from .ylnp import  e, pi, nan, inf, eps
from .ylnp import npFloatTypes, npIntTypes, npBoolTypes, npStrTypes
from .ylnp import savenp, loadnp, plot3dSurface, isNumpyType, testNumpyMultiprocessing

from .ylvector import sin, cos, arccos, arctan, deg2rad, rad2deg
from .ylvector import Vector, v0

from .ylstatistics import distavg, distnorm