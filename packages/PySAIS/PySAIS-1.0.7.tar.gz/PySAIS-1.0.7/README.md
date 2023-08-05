# PySAIS #

PySAIS is a wrapper to [Yuta Mori's](https://sites.google.com/site/yuta256/sais) implementation of the induced sorting algorithm to create suffix arrays. Both 32 bit and 64 bit indices are supported and automatically recognised.


## Requirements ##
Cython and numpy. 


## Useful features ##
This wrapper will automatically reduce the size of the computed array to uint16 or uint32 if possible. This is necessary as the algorithm makes use of the sign bit. If required, this can be disabled with the flag to the main function, which may be required on low-memory systems.

Both numpy byte-arrays as well as native byte and string types can be sent to the SAIS module.


(Further documentation to be added soon.)

## Example ##

```
#!python

In [1]: from PySAIS import sais

In [2]: s = 'test1 test2'

In [3]: sa = sais(s)

In [4]: sa
Out[4]: array([ 5,  4, 10,  1,  7,  2,  8,  3,  9,  0,  6], dtype=uint16)

In [5]: for i in range(len(sa)):
   ...:     print(s[sa[i]:])
 test2
1 test2
2
est1 test2
est2
st1 test2
st2
t1 test2
t2
test1 test2
test2

```

## License ##
MIT - same as the original implementation, as this is just a wrapper. All files which originate from sais-lite retain their copyright notice, as follows.

sais-lite license:
```
The sais-lite copyright is as follows:

Copyright (c) 2008-2010 Yuta Mori All Rights Reserved.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
```

PySAIS license
```
Copyright (c) 2017 Alex Warwick Vesztrocy.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
```