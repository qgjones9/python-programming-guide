# [function annotation](https://docs.python.org/3.14/glossary.html#term-function-annotation)

An [annotation](../annotation/index.md) of a function parameter or return value.

Function annotations are usually used for
[type hints](../type-hint/index.md): for example, this function is expected to take two
[int](https://docs.python.org/3.14/library/functions.html#int) arguments and is also expected to have an `int`
return value:

```python
def sum_two_numbers(a: int, b: int) -> int:
   return a + b
```

Function annotation syntax is explained in section [Function definitions](https://docs.python.org/3.14/reference/compound_stmts.html#function).

See [variable annotation](../variable-annotation/index.md) and [PEP 484](https://peps.python.org/pep-0484/),
which describe this functionality.
Also see [Annotations Best Practices](https://docs.python.org/3.14/howto/annotations.html#annotations-howto)
for best practices on working with annotations.
