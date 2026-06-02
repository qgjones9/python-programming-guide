# [context variable](https://docs.python.org/3.14/glossary.html#term-context-variable)

A variable whose value depends on which context is the [current
context](../current-context/index.md).  Values are accessed via [contextvars.ContextVar](https://docs.python.org/3.14/library/contextvars.html#contextvars.ContextVar)
objects.  Context variables are primarily used to isolate state between
concurrent asynchronous tasks.
