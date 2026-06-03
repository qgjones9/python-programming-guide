# [dictionary view](https://docs.python.org/3.14/glossary.html#term-dictionary-view)

The objects returned from [dict.keys()](https://docs.python.org/3.14/library/stdtypes.html#dict.keys), [dict.values()](https://docs.python.org/3.14/library/stdtypes.html#dict.values), and
[dict.items()](https://docs.python.org/3.14/library/stdtypes.html#dict.items) are called dictionary views. They provide a dynamic
view on the dictionary’s entries, which means that when the dictionary
changes, the view reflects these changes. To force the
dictionary view to become a full list use `list(dictview)`.  See
[Dictionary view objects](https://docs.python.org/3.14/library/stdtypes.html#dict-views).
