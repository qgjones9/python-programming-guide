# [__future__ — Future statement definitions](https://docs.python.org/3/library/__future__.html)

[`__future__`](https://docs.python.org/3/library/__future__.html) documents **feature flags** activated by `from __future__ import feature`. Each flag changes parser or semantics for the rest of that module, enabling gradual adoption before defaults flip in a future Python release. Reference: [docs.python.org](https://docs.python.org/3/library/__future__.html).

---

## Active features (3.14)

| Feature | Effect |
|---------|--------|
| `annotations` | Store annotations as strings (PEP 563 legacy; being superseded by deferred evaluation in 3.14) |
| `barry_as_FLUFL` | Easter egg: `<>` inequality |
| `braces` | Easter egg: `SyntaxError: not a chance` |
| `generator_stop` | `StopIteration` inside generator becomes `RuntimeError` |
| `nested_scopes` | Historical; always on |
| `print_function` | Historical; `print` is a function |
| `unicode_literals` | Historical; str literals are Unicode |
| `division` | `/` true division |

Must appear near top of file (only docstring/comments before it).

---

## Example — unicode_literals

```python
# Goal: unicode_literals makes unprefixed str literals Unicode (historical flag)
from __future__ import unicode_literals

text = "café"
assert isinstance(text, str)
assert text == "café"
```

---

## Interaction with annotations (3.14+)

Python 3.14 defaults to **deferred annotation evaluation** (PEP 649). `from __future__ import annotations` still forces **stringified** annotations until that future import is removed. For introspection, prefer [`annotationlib`](../annotationlib-functionality-for-introspecting-annotations/index.md).

---

## Best practices

| Practice | Why |
|----------|-----|
| Avoid new **`__future__` imports** unless required | Defaults move forward each release |
| Document **per-module** future flags in library README | Consumers inherit semantics file-by-file |
| Use **`annotationlib`** instead of parsing string annotations | Robust across evaluation models |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Future import not first code | `SyntaxError` | Only module docstring may precede |
| Assuming flag affects imported modules | Scoped to single compilation unit | Each module opts in separately |

---

## See also

- [`annotationlib`](../annotationlib-functionality-for-introspecting-annotations/index.md) — annotation retrieval across semantics
- [Future statements](https://docs.python.org/3/reference/simple_stmts.html#future) — language reference grammar
