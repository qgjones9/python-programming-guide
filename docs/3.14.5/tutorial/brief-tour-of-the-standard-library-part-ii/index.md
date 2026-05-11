# [Brief Tour of the Standard Library — Part II](https://docs.python.org/3/tutorial/stdlib2.html)

Condensed notes for [chapter 11](https://docs.python.org/3/tutorial/stdlib2.html): **`reprlib`**, **`textwrap`**, **`string.Template`**, **`struct`**, threading basics, **`logging`**, **`weakref`**, **`bisect`**, **`array`**, **`copy`**, **`pprint`**, **`decimal`**, and more. Follow the official page for full recipes.

```python
import textwrap

# `dedent` removes a common leading whitespace margin from multiline strings.
raw = """
    line1
    line2
"""
assert textwrap.dedent(raw).strip().startswith("line1")
```

```python
from decimal import Decimal

# Decimal avoids binary float surprises for money-like values.
assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
```

## Sections in this repo

- [Output Formatting](output-formatting/index.md)
- [Templating](templating/index.md)
- [Working with Binary Data Record Layouts](working-with-binary-data-record-layouts/index.md)
- [Multi-threading](multi-threading/index.md)
- [Logging](logging/index.md)
- [Weak References](weak-references/index.md)
- [Tools for Working with Lists](tools-for-working-with-lists/index.md)
- [Decimal floating-point arithmetic](decimal-floating-point-arithmetic/index.md)

Next: [Virtual Environments and Packages](../virtual-environments-and-packages/index.md)
