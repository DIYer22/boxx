from random import randint
from boxx import p
s = 'ABCD'
sample = s[p/randint(0, 3)] 
# print the output of randint(0, 3)
p-('sample is "%s"'%sample)
