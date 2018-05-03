# -*- coding: utf-8 -*-
from boxx import *
from boxx.tool.toolSystem import *
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
#TEST_ALL = False
 

testFun = None

tests = [testFun]
df=pd.DataFrame([{'a':5,'b':3},{1:1}]*20)
    
#tests = getArgvDic    
if ifTest(getArgvDic):    
    argv = ['toolTest.py', 
    '--name', 'name', 
    '--lr', '.23',
    '--resume', '21',
    '--posi','-50',
    '--pf','-6.98',]
    argv = ['toolTest.py', 
            'name.config', 
            'abc',
    '--lr', '.23',
    '--resume', 
    '--pf','-6.98',
    '--posi',]
    getArgvDic(argv)


#tests = heatMap    
if ifTest(heatMap):    
    code = '''
n=1000
b=map(pow,range(n),range(n))
c=map(divmod,b,b)
    '''
    heatMap(code)
#    heatMap('ylimgTest.py')
    
#tests = listdirWithFun
if ifTest(listdirWithFun): 
    def f(path):
        if '.py' not in path:
            log(path)
    listdirWithFun(root='..',fun=f)

def logr(s):
    sys.stdout.flush()
    log('\r%s'%s, end=' ')
#tests = logr
if ifTest(logr): 
    n=5
    for i in range(n):
        logr('%s [%s>%s]'%(i,'='*(i+1),' '*(n-i-1)))
        time.sleep(.2)
        
#tests = multiThread
if ifTest(multiThread): 
    mt = multiThread(5)
    def f(i):
        time.sleep(.01)
#        if i==20:
#            raise Exception,'test'
        log('%d '%i, end=' ')
    for i in range(100):
        mt(f,i)
    pred('[fanished befor join]')
    mt.join()
    pred('[fanished after join]')
    l=[]
    def ff(i):
#        if i==4:
#            raise Exception,'test ff'
        l.append(i)
        time.sleep(.1)
    for i in range(12):
        mt(ff,i)
    l.append('b')
    mt.join()
    l.append('a')
    print(l)
    

#tests = mapmp
if ifTest(mapmp): 
    import multiprocessing as mp
    mpd = mp.dummy
    def npt(rr):
        for i in range(int(4e3)):
            rr = abs(rr**0.9-rr)
        return rr.sum()
    n = 10
    rrs = [np.float64(randomm(20,90)) for i in range(n)]
    ms = {'map':map,'mapmt':mapmt,'mapmp':mapmp}
    for name,mapp in list(ms.items()):
        with timeit():
            list(mapp(npt,rrs))
            log(name, end=' ')

#tests = dira
if ifTest(dira): 
    import pandas
    dira(tool, pattern="^[A-Z]")
    dira(pandas.DataFrame(), pattern="^[A-Z]")
    dira(dicto(a=5,b=6), pattern="^va")
    what([0,{'k':'v'}])

#tests = pipe
#if ifTest(pipe):
    funList = [lambda x:x+'[f1]',lambda x:x+'[f2]',lambda x:x+'[f3]']
    do = pipe(funList)
    print((do('start')))

#tests = [wp, p]
if ifTest(wp):
    def fff( a=5):
        inf = 6
        p()
#        log-prettyFrameLocation(4)
    def ff():
        with wp:
            fff()
            fout=0
            with wp:
                fin = 1
    ff()

tests = [wp, p]
if ifTest(p):
    def fff(argfff=55):
        inf = 66
        out()
    def ff():
        fff()
    ff()
if __name__ == '__main__':
    pass

