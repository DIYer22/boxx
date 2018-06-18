from boxx import wgg
from random import randint
def f():
    other_vars = "No need to pay attention"
    with wgg:
        a = randint(1, 9)
        l = [a, a*2]
    others = "No need to pay attention" 
f()

# I want to transport and print `a` and `l` in f

