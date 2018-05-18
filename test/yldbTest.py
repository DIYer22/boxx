# -*- coding: utf-8 -*-
from boxx.yldb import *

'''
使用`ifTest([funName]) or 0:`来判断是否执行测试
这样 在测试过程中可以在iPython 查看每一个变量
'''
def ifTest(fun):
    shouldTest = fun is tests or (isinstance(tests,list) and fun in tests) or TEST_ALL 
    if shouldTest:
        try:
            pred('Test:'+ fun.__name__);log('Type:'+ str(type(fun)))
            log('Doc :'+ fun.__doc__)
        except Exception:
            pass
    return shouldTest

TEST_ALL = True
TEST_ALL = False


testFun = None

tests = [testFun]

#tests = GenSimg    
if ifTest(Evalu) or 0:
    
    pass


if __name__ == '__main__':

    pass




