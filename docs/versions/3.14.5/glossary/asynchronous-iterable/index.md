# [asynchronous iterable](https://docs.python.org/3.14/glossary.html#term-asynchronous-iterable)

An object, that can be used in an [asyncfor](https://docs.python.org/3.14/reference/compound_stmts.html#async-for) statement.
Must return an [asynchronous iterator](../asynchronous-iterator/index.md) from its
[__aiter__()](https://docs.python.org/3.14/reference/datamodel.html#object.__aiter__) method.  Introduced by [PEP 492](https://peps.python.org/pep-0492/).
