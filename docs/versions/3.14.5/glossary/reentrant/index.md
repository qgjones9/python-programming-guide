# [reentrant](https://docs.python.org/3.14/glossary.html#term-reentrant)

A property of a function or [lock](../lock/index.md) that allows it to be called or acquired multiple times by the same thread without causing errors or a [deadlock](../deadlock/index.md).

For functions, reentrancy means the function can be safely called again before a previous invocation has completed, which is important when functions may be called recursively or from signal handlers. Thread-unsafe functions may be [non-deterministic](../non-deterministic/index.md) if they’re called reentrantly in a multithreaded program.

For locks, Python’s [threading.RLock](https://docs.python.org/3.14/library/threading.html#threading.RLock) (reentrant lock) is reentrant, meaning a thread that already holds the lock can acquire it again without blocking.  In contrast, [threading.Lock](https://docs.python.org/3.14/library/threading.html#threading.Lock) is not reentrant - attempting to acquire it twice from the same thread will cause a deadlock.

See also [lock](../lock/index.md) and [deadlock](../deadlock/index.md).

