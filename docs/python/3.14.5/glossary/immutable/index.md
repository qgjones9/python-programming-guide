# [immutable](https://docs.python.org/3.14/glossary.html#term-immutable)

An object with a fixed value.  Immutable objects include numbers, strings and
tuples.  Such an object cannot be altered.  A new object has to
be created if a different value has to be stored.  They play an important
role in places where a constant hash value is needed, for example as a key
in a dictionary.  Immutable objects are inherently [thread-safe](../thread-safe/index.md)
because their state cannot be modified after creation, eliminating concerns
about improperly synchronized [concurrent modification](../concurrent-modification/index.md).
