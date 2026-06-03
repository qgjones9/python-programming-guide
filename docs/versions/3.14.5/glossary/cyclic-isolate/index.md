# [cyclic isolate](https://docs.python.org/3.14/glossary.html#term-cyclic-isolate)

A subgroup of one or more objects that reference each other in a reference
cycle, but are not referenced by objects outside the group.  The goal of
the [cyclic garbage collector](../garbage-collection/index.md) is to identify these groups and break the reference
cycles so that the memory can be reclaimed.
