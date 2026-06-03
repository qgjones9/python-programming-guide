# [variable annotation](https://docs.python.org/3.14/glossary.html#term-variable-annotation)

An [annotation](../annotation/index.md) of a variable or a class attribute.

When annotating a variable or a class attribute, assignment is optional:

```python
class C:
    field: 'annotation'
```

Variable annotations are usually used for
[type hints](../type-hint/index.md): for example this variable is expected to take
[int](https://docs.python.org/3.14/library/functions.html#int) values:

```python
count: int = 0
```

Variable annotation syntax is explained in section [Annotated assignment statements](https://docs.python.org/3.14/reference/simple_stmts.html#annassign).

See [function annotation](../function-annotation/index.md), [PEP 484](https://peps.python.org/pep-0484/)
and [PEP 526](https://peps.python.org/pep-0526/), which describe this functionality.
Also see [Annotations Best Practices](https://docs.python.org/3.14/howto/annotations.html#annotations-howto)
for best practices on working with annotations.
