# [named tuple](https://docs.python.org/3.14/glossary.html#term-named-tuple)

The term “named tuple” applies to any type or class that inherits from
tuple and whose indexable elements are also accessible using named
attributes.  The type or class may have other features as well.

Several built-in types are named tuples, including the values returned
by [time.localtime()](https://docs.python.org/3.14/library/time.html#time.localtime) and [os.stat()](https://docs.python.org/3.14/library/os.html#os.stat).  Another example is
[sys.float_info](https://docs.python.org/3.14/library/sys.html#sys.float_info):

```python
>>> sys.float_info[1]                   # indexed access
1024
>>> sys.float_info.max_exp              # named field access
1024
>>> isinstance(sys.float_info, tuple)   # kind of tuple
True
```

Some named tuples are built-in types (such as the above examples).
Alternatively, a named tuple can be created from a regular class
definition that inherits from [tuple](https://docs.python.org/3.14/library/stdtypes.html#tuple) and that defines named
fields.  Such a class can be written by hand, or it can be created by
inheriting [typing.NamedTuple](https://docs.python.org/3.14/library/typing.html#typing.NamedTuple), or with the factory function
[collections.namedtuple()](https://docs.python.org/3.14/library/collections.html#collections.namedtuple).  The latter techniques also add some
extra methods that may not be found in hand-written or built-in named
tuples.
