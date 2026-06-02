# [annotation](https://docs.python.org/3.14/glossary.html#term-annotation)

A label associated with a variable, a class
attribute or a function parameter or return value,
used by convention as a [type hint](../type-hint/index.md).

Annotations of local variables cannot be accessed at runtime, but
annotations of global variables, class attributes, and functions
can be retrieved by calling [annotationlib.get_annotations()](https://docs.python.org/3.14/library/annotationlib.html#annotationlib.get_annotations)
on modules, classes, and functions, respectively.

See [variable annotation](../variable-annotation/index.md), [function annotation](../function-annotation/index.md), [PEP 484](https://peps.python.org/pep-0484/),
[PEP 526](https://peps.python.org/pep-0526/), and [PEP 649](https://peps.python.org/pep-0649/), which describe this functionality.
Also see [Annotations Best Practices](https://docs.python.org/3.14/howto/annotations.html#annotations-howto)
for best practices on working with annotations.
