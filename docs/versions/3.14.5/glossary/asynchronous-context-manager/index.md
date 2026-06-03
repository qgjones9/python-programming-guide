# [asynchronous context manager](https://docs.python.org/3.14/glossary.html#term-asynchronous-context-manager)

An object which controls the environment seen in an [asyncwith](https://docs.python.org/3.14/reference/compound_stmts.html#async-with) statement by defining [__aenter__()](https://docs.python.org/3.14/reference/datamodel.html#object.__aenter__) and [__aexit__()](https://docs.python.org/3.14/reference/datamodel.html#object.__aexit__) methods.  Introduced by [PEP 492](https://peps.python.org/pep-0492/).
