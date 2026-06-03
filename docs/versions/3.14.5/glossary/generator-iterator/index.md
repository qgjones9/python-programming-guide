# [generator iterator](https://docs.python.org/3.14/glossary.html#term-generator-iterator)

An object created by a [generator](../generator/index.md) function.

Each [yield](https://docs.python.org/3.14/reference/simple_stmts.html#yield) temporarily suspends processing, remembering the execution state (including local variables and pending try-statements).  When the *generator iterator* resumes, it picks up where it left off (in contrast to functions which start fresh on every invocation).
