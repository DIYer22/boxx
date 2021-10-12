# -*- coding: utf-8 -*-
"""
tools for pandas 

@author: yl
"""

from __future__ import unicode_literals
import pandas as pd

def df2dicts(df, inculdeIndex=False):
    '''
    input a df, return to a list of dict
    
    Parameters
    ----------
    df : DataFrame
        pandas.DataFrame
    inculdeIndex : bool, default False
        return dic include index
    '''
    dicts = [dict(row) for index,row in df.iterrows()]
    if inculdeIndex:
        for index, dic in zip(df.index, dicts):
            dic['index'] = index
    return dicts

if __name__ == '__main__':
    pass
    df = pd.DataFrame({
                       0:list(range(5)),
                       1:list(range(10,15)),
                       'a':list("abcde"),
                       })
    df.set_index(0,inplace=True)

