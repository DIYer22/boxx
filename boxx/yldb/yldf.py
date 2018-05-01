# -*- coding: utf-8 -*-

from __future__ import unicode_literals


if __name__ == '__main__':
    pass
    import pandas as pd
    df = pd.DataFrame({
                       0:list(range(5)),
                       1:list(range(10,15)),
                       'a':list("abcde"),
                       })
    df.set_index(0,inplace=True)

