'''
    Python interface to optimised SAIS implementation by ...

    Note: this is for 64 bit indices suffix array construction.

    -- Alex Warwick Vesztrocy, March 2017
'''
from libc.string cimport const_uchar
from tables.earray import EArray
import numpy as np
cimport numpy as np
cimport python_unicode
cimport stdlib


# Define the type for this SAIS
ctypedef np.int64_t DTYPE_t
DTYPE = np.int64


cdef extern from "sais64.h":
    int _sais(const_uchar *T, DTYPE_t *SA, DTYPE_t n) nogil


cdef _sais_c(unsigned char *t, DTYPE_t[::1] sa, DTYPE_t n):
    with nogil:
        r = _sais(&t[0], &sa[0], n)
    if r < 0:
        raise RuntimeError('Error in SAIS')

def sais(s):
    '''
        Generate the suffix array using the SAIS algorithm from
        bytes, or from an EArray of bytes (from PyTables).
    '''
    cdef unsigned char* t = s
    n = len(s)

    # Declare the suffix array
    sa = np.zeros(n, dtype=DTYPE)

    # Run SAIS
    _sais_c(t, sa, n)

    return sa
