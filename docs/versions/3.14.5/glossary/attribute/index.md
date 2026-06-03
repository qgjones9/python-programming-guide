# [attribute](https://docs.python.org/3.14/glossary.html#term-attribute)

A value associated with an object which is usually referenced by name using dotted expressions. For example, if an object *o* has an attribute *a* it would be referenced as *o.a*.

It is possible to give an object an attribute whose name is not an identifier as defined by [Names (identifiers and keywords)](https://docs.python.org/3.14/reference/lexical_analysis.html#identifiers), for example using [setattr()](https://docs.python.org/3.14/library/functions.html#setattr), if the object allows it. Such an attribute will not be accessible using a dotted expression, and would instead need to be retrieved with [getattr()](https://docs.python.org/3.14/library/functions.html#getattr).
