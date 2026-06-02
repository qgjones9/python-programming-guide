# [deadlock](https://docs.python.org/3.14/glossary.html#term-deadlock)

A situation in which two or more tasks (threads, processes, or coroutines)
wait indefinitely for each other to release resources or complete actions,
preventing any from making progress.  For example, if thread A holds lock
1 and waits for lock 2, while thread B holds lock 2 and waits for lock 1,
both threads will wait indefinitely.  In Python this often arises from
acquiring multiple locks in conflicting orders or from circular
join/await dependencies.  Deadlocks can be avoided by always acquiring
multiple [locks](../lock/index.md) in a consistent order.  See also
lock and [reentrant](../reentrant/index.md).
