# [non-deterministic](https://docs.python.org/3.14/glossary.html#term-non-deterministic)

Behavior where the outcome of a program can vary between executions with the same inputs.  In multi-threaded programs, non-deterministic behavior often results from [race conditions](../race-condition/index.md) where the relative timing or interleaving of threads affects the result. Proper synchronization using [locks](../lock/index.md) and other [synchronization primitives](../synchronization-primitive/index.md) helps ensure deterministic behavior.
