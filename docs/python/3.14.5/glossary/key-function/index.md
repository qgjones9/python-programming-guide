# [key function](https://docs.python.org/3.14/glossary.html#term-key-function)

A key function or collation function is a callable that returns a value
used for sorting or ordering.  For example, [locale.strxfrm()](https://docs.python.org/3.14/library/locale.html#locale.strxfrm) is
used to produce a sort key that is aware of locale specific sort
conventions.

A number of tools in Python accept key functions to control how elements
are ordered or grouped.  They include [min()](https://docs.python.org/3.14/library/functions.html#min), [max()](https://docs.python.org/3.14/library/functions.html#max),
[sorted()](https://docs.python.org/3.14/library/functions.html#sorted), [list.sort()](https://docs.python.org/3.14/library/stdtypes.html#list.sort), [heapq.merge()](https://docs.python.org/3.14/library/heapq.html#heapq.merge),
[heapq.nsmallest()](https://docs.python.org/3.14/library/heapq.html#heapq.nsmallest), [heapq.nlargest()](https://docs.python.org/3.14/library/heapq.html#heapq.nlargest), and
[itertools.groupby()](https://docs.python.org/3.14/library/itertools.html#itertools.groupby).

There are several ways to create a key function.  For example. the
[str.casefold()](https://docs.python.org/3.14/library/stdtypes.html#str.casefold) method can serve as a key function for case insensitive
sorts.  Alternatively, a key function can be built from a
[lambda](https://docs.python.org/3.14/reference/expressions.html#lambda) expression such as `lambda r: (r[0], r[2])`.  Also,
[operator.attrgetter()](https://docs.python.org/3.14/library/operator.html#operator.attrgetter), [operator.itemgetter()](https://docs.python.org/3.14/library/operator.html#operator.itemgetter), and
[operator.methodcaller()](https://docs.python.org/3.14/library/operator.html#operator.methodcaller) are three key function constructors.  See the [Sorting HOW TO](https://docs.python.org/3.14/howto/sorting.html#sortinghowto) for examples of how to create and use key functions.
