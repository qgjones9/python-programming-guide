# [list comprehension](https://docs.python.org/3.14/glossary.html#term-list-comprehension)

A compact way to process all or part of the elements in a sequence and
return a list with the results.  `result = ['{:#04x}'.format(x) for x in
range(256) if x % 2 == 0]` generates a list of strings containing
even hex numbers (0x..) in the range from 0 to 255. The [if](https://docs.python.org/3.14/reference/compound_stmts.html#if)
clause is optional.  If omitted, all elements in `range(256)` are
processed.
