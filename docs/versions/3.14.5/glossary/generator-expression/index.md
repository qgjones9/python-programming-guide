# [generator expression](https://docs.python.org/3.14/glossary.html#term-generator-expression)

An [expression](../expression/index.md) that returns an [iterator](../iterator/index.md).  It looks like a normal expression followed by a `for` clause defining a loop variable, range, and an optional `if` clause.  The combined expression generates values for an enclosing function:

```python
>>> sum(i*i for i in range(10))         # sum of squares 0, 1, 4, ... 81
285
```
