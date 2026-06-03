# [free variable](https://docs.python.org/3.14/glossary.html#term-free-variable)

Formally, as defined in the [language execution model](https://docs.python.org/3.14/reference/executionmodel.html#bind-names), a free variable is any variable used in a namespace which is not a local variable in that namespace. See [closure variable](../closure-variable/index.md) for an example.

Pragmatically, due to the name of the [codeobject.co_freevars](https://docs.python.org/3.14/reference/datamodel.html#codeobject.co_freevars) attribute, the term is also sometimes used as a synonym for closure variable.
