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
        print('{}(*{}, **{}): {:,.0f} tps, {:.2f} us/txn'
                .format(f.__name__, args, kw, 1.0/latency, latency*1000000.0))
        return result
    return wrap

@timing
def expdecay(i, x=0.5, factor=1.0):
    for _ in rng(i):
        y = math.exp(-factor*x)
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

    for f in [expdecay, cy_expdecay, cya_expdecay, cy_expdecay2, cya_expdecay2]:
        f(i)
