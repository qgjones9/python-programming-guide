# [atomic operation](https://docs.python.org/3.14/glossary.html#term-atomic-operation)

An operation that appears to execute as a single, indivisible step: no
other thread can observe it half-done, and its effects become visible all
at once.  Python does not guarantee that high-level statements are atomic
(for example, `x += 1` performs multiple bytecode operations and is not
atomic).  Atomicity is only guaranteed where explicitly documented.  See
also [race condition](../race-condition/index.md) and [data race](../data-race/index.md).
