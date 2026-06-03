# [contiguous](https://docs.python.org/3.14/glossary.html#term-contiguous)

A buffer is considered contiguous exactly if it is either *C-contiguous* or *Fortran contiguous*.  Zero-dimensional buffers are C and Fortran contiguous.  In one-dimensional arrays, the items must be laid out in memory next to each other, in order of increasing indexes starting from zero.  In multidimensional C-contiguous arrays, the last index varies the fastest when visiting items in order of memory address.  However, in Fortran contiguous arrays, the first index varies the fastest.
