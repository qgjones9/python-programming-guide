# [LBYL](https://docs.python.org/3.14/glossary.html#term-LBYL)

Look before you leap.  This coding style explicitly tests for
pre-conditions before making calls or lookups.  This style contrasts with
the [EAFP](../EAFP/index.md) approach and is characterized by the presence of many
[if](https://docs.python.org/3.14/reference/compound_stmts.html#if) statements.

In a multi-threaded environment, the LBYL approach can risk introducing a
[race condition](../race-condition/index.md) between “the looking” and “the leaping”.  For example,
the code, `if key in mapping: return mapping[key]` can fail if another
thread removes *key* from *mapping* after the test, but before the lookup.
This issue can be solved with [locks](../lock/index.md) or by using the
[EAFP](../EAFP/index.md) approach.  See also [thread-safe](../thread-safe/index.md).
