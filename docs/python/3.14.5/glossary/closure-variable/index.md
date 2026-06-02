# [closure variable](https://docs.python.org/3.14/glossary.html#term-closure-variable)

A [free variable](../free-variable/index.md) referenced from a [nested scope](../nested-scope/index.md) that is defined in an outer
scope rather than being resolved at runtime from the globals or builtin namespaces.
May be explicitly defined with the [nonlocal](https://docs.python.org/3.14/reference/simple_stmts.html#nonlocal) keyword to allow write access,
or implicitly defined if the variable is only being read.

For example, in the `inner` function in the following code, both `x` and `print` are
[free variables](../free-variable/index.md), but only `x` is a *closure variable*:

```python
def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        print(x)
    return inner
```

Due to the [codeobject.co_freevars](https://docs.python.org/3.14/reference/datamodel.html#codeobject.co_freevars) attribute (which, despite its name, only
includes the names of closure variables rather than listing all referenced free
variables), the more general [free variable](../free-variable/index.md) term is sometimes used even
when the intended meaning is to refer specifically to closure variables.
