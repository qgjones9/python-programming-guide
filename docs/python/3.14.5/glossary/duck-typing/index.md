# [duck-typing](https://docs.python.org/3.14/glossary.html#term-duck-typing)

A programming style which does not look at an object’s type to determine
if it has the right interface; instead, the method or attribute is simply
called or used (“If it looks like a duck and quacks like a duck, it
must be a duck.”)  By emphasizing interfaces rather than specific types,
well-designed code improves its flexibility by allowing polymorphic
substitution.  Duck-typing avoids tests using [type()](https://docs.python.org/3.14/library/functions.html#type) or
[isinstance()](https://docs.python.org/3.14/library/functions.html#isinstance).  (Note, however, that duck-typing can be complemented
with [abstract base classes](../abstract-base-class/index.md).)  Instead, it
typically employs [hasattr()](https://docs.python.org/3.14/library/functions.html#hasattr) tests or [EAFP](../EAFP/index.md) programming.
