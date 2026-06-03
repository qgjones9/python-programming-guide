# [asynchronous generator iterator](https://docs.python.org/3.14/glossary.html#term-asynchronous-generator-iterator)

An object created by an [asynchronous generator](../asynchronous-generator/index.md) function.

This is an [asynchronous iterator](../asynchronous-iterator/index.md) which when called using the [__anext__()](https://docs.python.org/3.14/reference/datamodel.html#object.__anext__) method returns an awaitable object which will execute the body of the asynchronous generator function until the next [yield](https://docs.python.org/3.14/reference/simple_stmts.html#yield) expression.

Each [yield](https://docs.python.org/3.14/reference/simple_stmts.html#yield) temporarily suspends processing, remembering the execution state (including local variables and pending try-statements).  When the *asynchronous generator iterator* effectively resumes with another awaitable returned by [__anext__()](https://docs.python.org/3.14/reference/datamodel.html#object.__anext__), it picks up where it left off.  See [PEP 492](https://peps.python.org/pep-0492/) and [PEP 525](https://peps.python.org/pep-0525/).
