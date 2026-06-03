# [race condition](https://docs.python.org/3.14/glossary.html#term-race-condition)

A condition of a program where the behavior
depends on the relative timing or ordering of events, particularly in
multi-threaded programs.  Race conditions can lead to
[non-deterministic](../non-deterministic/index.md) behavior and bugs that are difficult to
reproduce.  A [data race](../data-race/index.md) is a specific type of race condition
involving unsynchronized access to shared memory.  The [LBYL](../LBYL/index.md)
coding style is particularly susceptible to race conditions in
multi-threaded code.  Using [locks](../lock/index.md) and other
[synchronization primitives](../synchronization-primitive/index.md)
helps prevent race conditions.
