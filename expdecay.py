from __future__ import print_function
from functools import wraps
import math
import sys
from time import time

# Setup cython modules
import pyximport; pyximport.install()
import cyexpdecay

rng = xrange if sys.version_info.major < 3 else range

i = 1000000

def timing(f):
    '''See: http://stackoverflow.com/a/27737385'''
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        latency = (te-ts)/i

        # Mangle function to display
        func = '{}(*{}, **{})'.format(f.__name__, args, kw)
        maxlen=32
        if len(func) > maxlen:
            func = func[:maxlen-3] + '...'
        else:
            func = func + ' '* (maxlen-len(func))

        print('{}\t{:,.1f} mtps\t{:.2f} us/txn'
                .format(func, 1.0/(latency*1000000.0), latency*1000000.0))

        return result
    return wrap

@timing
def expdecay(i, x=0.5, factor=1.0):
    for _ in rng(i):
        y = math.exp(-factor*x)
    return y

def expdecay2(x=0.5, factor=1.0):
    return math.exp(-factor*x)

@timing
def time_expdecay2(i):
    for _ in rng(i):
        y = expdecay2()
    return y

cy_expdecay = timing(cyexpdecay.cy_expdecay)
cya_expdecay = timing(cyexpdecay.cya_expdecay)

@timing
def cy_expdecay2(i):
    for _ in rng(i):
        y = cyexpdecay.cy_expdecay2()
    return y

@timing
def cya_expdecay2(i):
    for _ in rng(i):
        y = cyexpdecay.cya_expdecay2()
    return y

if __name__ == '__main__':
    try: 
        i = int(sys.argv[1])
    except Exception as e:
        pass

    for f in [expdecay, cy_expdecay, cya_expdecay, time_expdecay2, cy_expdecay2, cya_expdecay2]:
        f(i)
