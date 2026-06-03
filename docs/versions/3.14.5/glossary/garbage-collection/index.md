# [garbage collection](https://docs.python.org/3.14/glossary.html#term-garbage-collection)

The process of freeing memory when it is not used anymore.  Python performs garbage collection via reference counting and a cyclic garbage collector that is able to detect and break reference cycles.  The garbage collector can be controlled using the [gc](https://docs.python.org/3.14/library/gc.html#module-gc) module.
