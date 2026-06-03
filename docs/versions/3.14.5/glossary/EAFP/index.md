# [EAFP](https://docs.python.org/3.14/glossary.html#term-EAFP)

Easier to ask for forgiveness than permission.  This common Python coding style assumes the existence of valid keys or attributes and catches exceptions if the assumption proves false.  This clean and fast style is characterized by the presence of many [try](https://docs.python.org/3.14/reference/compound_stmts.html#try) and [except](https://docs.python.org/3.14/reference/compound_stmts.html#except) statements.  The technique contrasts with the [LBYL](../LBYL/index.md) style common to many other languages such as C.
