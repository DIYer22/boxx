# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class dictToObj(dict):
    '''
    将dic转换为可以用dic模式访问的obj
    '''
    def __init__(self, dic):
        dict.__init__(self)
#        self.dic = dic
        for k,v in list(dic.items()):
            setattr(self,k,v)
    def __getitem__(self,k):
        return getattr(self,k)
    def __setitem__(self,k,v):
        return setattr(self,k,v)






