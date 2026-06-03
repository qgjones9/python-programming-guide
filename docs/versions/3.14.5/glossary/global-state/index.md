# [global state](https://docs.python.org/3.14/glossary.html#term-global-state)

Data that is accessible throughout a program, such as module-level variables, class variables, or C static variables in [extension modules](../extension-module/index.md).  In multi-threaded programs, global state shared between threads typically requires synchronization to avoid [race conditions](../race-condition/index.md) and [data races](../data-race/index.md).
