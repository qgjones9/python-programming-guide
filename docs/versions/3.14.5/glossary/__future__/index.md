# [__future__](https://docs.python.org/3.14/glossary.html#term-__future__)

A [future statement](https://docs.python.org/3.14/reference/simple_stmts.html#future), `from __future__ import <feature>`, directs the compiler to compile the current module using syntax or semantics that will become standard in a future release of Python.

The [__future__](https://docs.python.org/3.14/library/__future__.html#module-__future__) module documents the possible values of *feature*.  By importing this module and evaluating its variables, you can see when a new feature was first added to the language and when it will (or did) become the default:

```python
>>> import __future__
>>> __future__.division
_Feature((2, 2, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0), 8192)
```
