# [immortal](https://docs.python.org/3.14/glossary.html#term-immortal)

*Immortal objects* are a CPython implementation detail introduced
in [PEP 683](https://peps.python.org/pep-0683/).

If an object is immortal, its [reference count](../reference-count/index.md) is never modified,
and therefore it is never deallocated while the interpreter is running.
For example, [True](https://docs.python.org/3.14/library/constants.html#True) and [None](https://docs.python.org/3.14/library/constants.html#None) are immortal in CPython.

Immortal objects can be identified via [sys._is_immortal()](https://docs.python.org/3.14/library/sys.html#sys._is_immortal), or
via [PyUnstable_IsImmortal()](https://docs.python.org/3.14/c-api/object.html#c.PyUnstable_IsImmortal) in the C API.
