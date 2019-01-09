#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Wed Jan  9 23:24:20 2019
"""
import pandas as pd
import numpy as np

class Markdown(pd.DataFrame):
    '''
    Markdown class base on DataFrame
    '''
    def __round__(self, *l, **kv):
        redf = pd.DataFrame.__round__(self, *l, **kv)
        return Markdown(redf)
    
    def round(self, *l, **kv):
        redf = pd.DataFrame.round(self, *l, **kv)
        return Markdown(redf)
        
    def to_md(df, nblankBetweenCell=1, tableMidSymbol = "---:"):
        '''
        Transfer DataFrame to markdown
        
        Parameters
        ----------
        df : DataFrame
            pandas.DataFrame
        
        nblankBetweenCell : int, default 1
            How many blanks between 2 cells
        tableMidSymbol : str, default "---:"
            "-:", ":-", ":-:" for markdown 
        
        '''
        blanks = nblankBetweenCell *" "
        betweenCell = blanks + "|" + blanks
        rowFormat = "|%s%s%s|" % (blanks, "%s", blanks)
        ncols = len(df.columns)
        strcols = df.columns.map(str)
        lencols = np.array(strcols.map(len))
        
        strdf = df.applymap(str)
        lendf = np.array(strdf.applymap(len))
        
        
        maxLens = np.array(list(zip(lendf.max(0), lencols, [len(tableMidSymbol)]*ncols))).max(1)
        
        vMulBlank = np.vectorize(lambda x:x * " ")

        mdcols = vMulBlank(maxLens - lencols) + strcols
        mddf = vMulBlank(maxLens - lendf)  + strdf
        
        headstr = rowFormat % betweenCell.join(mdcols)
        
        tableMidStr = rowFormat% betweenCell.join(map(lambda x: x + tableMidSymbol, vMulBlank(maxLens-len(tableMidSymbol))))
        
        bodystr = "\n".join(map(lambda kv: rowFormat% betweenCell.join(kv[-1]), mddf.iterrows()))
        
        tablestr = '\n'.join([headstr, tableMidStr, bodystr])
        return tablestr
    def __str__(self):
        return self.to_md()
    
    @staticmethod
    def test():
        df = pd.DataFrame([{"a":1, "b":1,}, {"a":1, "bbbbbb":1,}, {"a":1, "bbbbbb":1/2, "c":1/3}])
        md = Markdown(df)
        print(md)
        print("-"*20)
        print(md.round(2))

if __name__ == "__main__":
    pass
    
    
    
