# [synchronization primitive](https://docs.python.org/3.14/glossary.html#term-synchronization-primitive)

A basic building block for coordinating (synchronizing) the execution of
multiple threads to ensure [thread-safe](../thread-safe/index.md) access to shared resources.
Python’s [threading](https://docs.python.org/3.14/library/threading.html#module-threading) module provides several synchronization primitives
including [Lock](https://docs.python.org/3.14/library/threading.html#threading.Lock), [RLock](https://docs.python.org/3.14/library/threading.html#threading.RLock),
[Semaphore](https://docs.python.org/3.14/library/threading.html#threading.Semaphore), [Condition](https://docs.python.org/3.14/library/threading.html#threading.Condition),
[Event](https://docs.python.org/3.14/library/threading.html#threading.Event), and [Barrier](https://docs.python.org/3.14/library/threading.html#threading.Barrier).  Additionally,
the [queue](https://docs.python.org/3.14/library/queue.html#module-queue) module provides multi-producer, multi-consumer queues
that are especially useful in multithreaded programs. These
primitives help prevent [race conditions](../race-condition/index.md) and
coordinate thread execution.  See also [lock](../lock/index.md).
