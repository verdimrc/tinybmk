from __future__ import print_function
from functools import wraps
import math
import sys
from time import time

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
        print('{}(*{}, **{}) took: {:,.0f} tps (i.e., {:.2f} us/txn)'
                .format(f.__name__, args, kw, 1.0/latency, latency*1000000.0))
        return result
    return wrap

@timing
def expdecay(i, x=0.5, factor=1.0):
    for _ in rng(i):
        y = math.exp(-factor*x)
    return y

if __name__ == '__main__':
    try: 
        i = int(sys.argv[1])
    except Exception as e:
        pass
    expdecay(i)
