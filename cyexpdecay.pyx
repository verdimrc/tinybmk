import math as pymath
import sys

from libc.math cimport exp

rng = xrange if sys.version_info.major < 3 else range

def cy_expdecay(i, x=0.5, factor=1.0):
    for _ in rng(i):
        y = pymath.exp(-factor*x)
    return y

cpdef double cya_expdecay(int i, double x=0.5, double factor=1.0):
    cdef int _
    cdef double y
    for _ in rng(i):
        y = exp(-factor*x)
    return y

def cy_expdecay2(x=0.5, factor=1.0):
    y = pymath.exp(-factor*x)
    return y

cpdef double cya_expdecay2(double x=0.5, double factor=1.0):
    cdef double y
    y = exp(-factor*x)
    return y
