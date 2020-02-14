#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statistics tools 

@author: yl
"""
import random
import numpy as np
from functools import wraps
from collections import Counter


def Distribution(f):
    """
    return  distribution of bias round v and max bias is @maxratio*v.mean() or @maxbias
    """

    @wraps(f)
    def innerF(v, maxbias=None, maxratio=0.2, *l, **kv):
        mean = v
        if maxbias is None:
            if isinstance(v, np.ndarray):
                mean = v.mean()
            maxbias = maxratio * mean
        biass = f(v=v, maxbias=maxbias, maxratio=maxratio, *l, **kv)
        return v + biass

    return innerF


@Distribution
def distnorm(v, maxbias=None, maxratio=0.2, std=2):
    """
    return normal distribution of bias round v and max bias is @maxratio*v.mean() or @maxbias
    """
    shape = None
    if isinstance(v, np.ndarray):
        shape = v.shape
    normaBiass = np.random.normal(loc=1, scale=1.0 / std, size=shape) % (2) - 1

    biass = normaBiass * maxbias
    return biass


@Distribution
def distavg(v, maxbias=None, maxratio=0.2):
    """
    return uniform distribution of bias round v and max bias is @maxratio*v.mean() or @maxbias
    """
    shape = None
    if isinstance(v, np.ndarray):
        shape = v.shape
    biass = np.random.uniform(-maxbias, maxbias, size=shape)
    return biass


class DiscreteSample(dict):
    def sample(self):
        summ = sum(self.values())
        random_number = random.random() * summ
        for k, v in self.items():
            random_number -= v
            if random_number <= 0:
                return k

    @staticmethod
    def test():
        ds = DiscreteSample({"a": 1, "b": 2, "c": 0})
        print(Counter([ds.sample() for _ in range(1000000)]))


class HeatmapSample:
    def __init__(self, heatmap):
        h, w = heatmap.shape
        hs, ws = np.mgrid[:h, :w]
        hs, ws = hs.reshape(-1), ws.reshape(-1)
        self.discrete_sample = DiscreteSample(zip(zip(hs, ws), heatmap.reshape(-1)))

    def sample(self):
        return self.discrete_sample.sample()


if __name__ == "__main__":
    from boxx import loga

    loga(distavg(np.ones((517, 111))))
    loga(distnorm(np.ones((517, 111)), 3, std=4))
    DiscreteSample.test()
    pass
