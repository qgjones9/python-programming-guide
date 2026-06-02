# [per-object lock](https://docs.python.org/3.14/glossary.html#term-per-object-lock)

A [lock](../lock/index.md) associated with an individual object instance rather than
a global lock shared across all objects. In [free-threaded](../free-threading/index.md) Python, built-in types like [dict](https://docs.python.org/3.14/library/stdtypes.html#dict) and
[list](https://docs.python.org/3.14/library/stdtypes.html#list) use per-object locks to allow concurrent operations on
different objects while serializing operations on the same object.
Operations that hold the per-object lock prevent other locking operations
on the same object from proceeding, but do not block [lock-free](../lock-free/index.md)
operations.
