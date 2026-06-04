# [7.11. The import statement](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)

Notes on **7.11. The import statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement).

- `import mod [as name]` finds/loads a module, then binds name(s) in the current namespace (like assignment).
- `from pkg import attr` loads `pkg`, resolves `attr` (possibly via submodule import), then binds locally.
- `from __future__ import …` is a compile-time *future statement* (see §7.11.1 on the canonical page).

```python
# import and from-import bind names in the current namespace.
import json as j

assert j.dumps([1]) == "[1]"

from collections import deque

d = deque([1, 2])
d.append(3)
assert list(d) == [1, 2, 3]
```

Parent: [7. Simple statements](../index.md)
