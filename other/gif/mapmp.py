def bad_fibonacci(x): # simulation Complex calculations
    return x<=1 or x*bad_fibonacci(x-1)

xs = [800]*10000

from boxx import mapmp
from boxx import timeit # for timing
with timeit('map'):
    resoult = map(bad_fibonacci, xs, )
    resoult = list(resoult)

#Note: I test this code on i5 CPU