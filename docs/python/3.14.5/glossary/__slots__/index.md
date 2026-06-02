# [__slots__](https://docs.python.org/3.14/glossary.html#term-__slots__)

A declaration inside a class that saves memory by pre-declaring space for
instance attributes and eliminating instance dictionaries.  Though
popular, the technique is somewhat tricky to get right and is best
reserved for rare cases where there are large numbers of instances in a
memory-critical application.
