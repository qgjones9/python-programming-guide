# [concurrent modification](https://docs.python.org/3.14/glossary.html#term-concurrent-modification)

When multiple threads modify shared data at the same time.  Concurrent modification without proper synchronization can cause [race conditions](../race-condition/index.md), and might also trigger a [data race](../data-race/index.md), data corruption, or both.
