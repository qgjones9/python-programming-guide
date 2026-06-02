# [asynchronous generator](https://docs.python.org/3.14/glossary.html#term-asynchronous-generator)

A function which returns an [asynchronous generator iterator](../asynchronous-generator-iterator/index.md).  It
looks like a coroutine function defined with [asyncdef](https://docs.python.org/3.14/reference/compound_stmts.html#async-def) except
that it contains [yield](https://docs.python.org/3.14/reference/simple_stmts.html#yield) expressions for producing a series of
values usable in an [asyncfor](https://docs.python.org/3.14/reference/compound_stmts.html#async-for) loop.

Usually refers to an asynchronous generator function, but may refer to an
*asynchronous generator iterator* in some contexts.  In cases where the
intended meaning isn’t clear, using the full terms avoids ambiguity.

An asynchronous generator function may contain [await](https://docs.python.org/3.14/reference/expressions.html#await)
expressions as well as [asyncfor](https://docs.python.org/3.14/reference/compound_stmts.html#async-for), and [asyncwith](https://docs.python.org/3.14/reference/compound_stmts.html#async-with)
statements.
