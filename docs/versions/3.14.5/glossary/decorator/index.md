# [decorator](https://docs.python.org/3.14/glossary.html#term-decorator)

A function returning another function, usually applied as a function transformation using the `@wrapper` syntax.  Common examples for decorators are [classmethod()](https://docs.python.org/3.14/library/functions.html#classmethod) and [staticmethod()](https://docs.python.org/3.14/library/functions.html#staticmethod).

The decorator syntax is merely syntactic sugar, the following two function definitions are semantically equivalent:

```python
def f(arg):
    ...
f = staticmethod(f)

@staticmethod
def f(arg):
    ...
```

The same concept exists for classes, but is less commonly used there.  See the documentation for [function definitions](https://docs.python.org/3.14/reference/compound_stmts.html#function) and [class definitions](https://docs.python.org/3.14/reference/compound_stmts.html#class) for more about decorators.
