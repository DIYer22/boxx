#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Fri Feb 15 20:20:59 2019
"""
from . import torch, hasnan


def pthnan(pth):
    dic = torch.load(pth, map_location='cpu')
    from collections import OrderedDict
    
    def getOrderedDict(seq):
        if isinstance(seq, OrderedDict):
            return seq
        if isinstance(seq, dict):
            seq = list(seq.values())
        if not isinstance(seq, (tuple, list)):
            return None
        for s in seq:
            re = getOrderedDict(s)
            if re is not None:
                return re
    od = getOrderedDict(dic)
    tensor = list(od.values())[-1]
    print('\n"%s"\n\nHas nan: %s\n'%('\x1b[36m%s\x1b[0m'%tensor[...,:10], '\x1b[31m%s\x1b[0m'%hasnan(tensor)))


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="""
    detect a pth file "Does it has nan?" """)
    parser.add_argument('pth', default='/home/dl/github/maskrcnn/output/mix_11/model_final.pth', type=str)
    args = parser.parse_args()
    
    pthnan(pth=args.pth)
    
