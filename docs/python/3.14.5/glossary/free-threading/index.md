# [free threading](https://docs.python.org/3.14/glossary.html#term-free-threading)

A threading model where multiple threads can run Python bytecode
simultaneously within the same interpreter.  This is in contrast to
the [global interpreter lock](../global-interpreter-lock/index.md) which allows only one thread to
execute Python bytecode at a time.  See [PEP 703](https://peps.python.org/pep-0703/).
