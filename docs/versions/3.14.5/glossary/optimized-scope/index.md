# [optimized scope](https://docs.python.org/3.14/glossary.html#term-optimized-scope)

A scope where target local variable names are reliably known to the
compiler when the code is compiled, allowing optimization of read and
write access to these names. The local namespaces for functions,
generators, coroutines, comprehensions, and generator expressions are
optimized in this fashion. Note: most interpreter optimizations are
applied to all scopes, only those relying on a known set of local
and nonlocal variable names are restricted to optimized scopes.
