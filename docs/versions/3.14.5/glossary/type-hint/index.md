# [type hint](https://docs.python.org/3.14/glossary.html#term-type-hint)

An [annotation](../annotation/index.md) that specifies the expected type for a variable, a class attribute, or a function parameter or return value.

Type hints are optional and are not enforced by Python but they are useful to [static type checkers](../static-type-checker/index.md). They can also aid IDEs with code completion and refactoring.

Type hints of global variables, class attributes, and functions, but not local variables, can be accessed using [typing.get_type_hints()](https://docs.python.org/3.14/library/typing.html#typing.get_type_hints).

See [typing](https://docs.python.org/3.14/library/typing.html#module-typing) and [PEP 484](https://peps.python.org/pep-0484/), which describe this functionality.

