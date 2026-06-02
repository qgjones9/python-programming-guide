# [thread-safe](https://docs.python.org/3.14/glossary.html#term-thread-safe)

A module, function, or class that behaves correctly when used by multiple
threads concurrently.  Thread-safe code uses appropriate
[synchronization primitives](../synchronization-primitive/index.md) like
[locks](../lock/index.md) to protect shared mutable state, or is designed
to avoid shared mutable state entirely.  In the
[free-threaded](../free-threading/index.md) build, built-in types like
[dict](https://docs.python.org/3.14/library/stdtypes.html#dict), [list](https://docs.python.org/3.14/library/stdtypes.html#list), and [set](https://docs.python.org/3.14/library/stdtypes.html#set) use internal locking
to make many operations thread-safe, although thread safety is not
necessarily guaranteed.  Code that is not thread-safe may experience
[race conditions](../race-condition/index.md) and [data races](../data-race/index.md)
when used in multi-threaded programs.
