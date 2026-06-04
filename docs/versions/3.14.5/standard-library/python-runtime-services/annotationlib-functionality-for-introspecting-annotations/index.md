# [annotationlib — Functionality for introspecting annotations](https://docs.python.org/3/library/annotationlib.html)

[`annotationlib`](https://docs.python.org/3/library/annotationlib.html) (Python **3.14+**) provides reliable **annotation introspection** across evaluation models: stock (eager), stringified (`from __future__ import annotations`), and **deferred evaluation** (PEP 649 default in 3.14). Main entry: `get_annotations()`. Reference: [docs.python.org](https://docs.python.org/3/library/annotationlib.html).

**Security:** many APIs can execute arbitrary code when resolving annotations — treat untrusted objects carefully.

---

## Format enum — [Classes](https://docs.python.org/3/library/annotationlib.html#classes)

| `Format` | Returns |
|----------|---------|
| `VALUE` | Evaluated annotation objects |
| `FORWARDREF` | Real values where possible; `ForwardRef` proxies for unresolved names |
| `STRING` | Source-like annotation text |

Pass `format=` to `get_annotations()` and related helpers.

---

## Deferred evaluation (3.14 default)

Forward references to not-yet-defined classes resolve when accessed under deferred semantics — unlike stock 3.13 behavior that raised `NameError` at function definition time.

```python
# Goal: forward reference resolves under 3.14 deferred annotations
import sys

if sys.version_info >= (3, 14):
    import annotationlib

    def func(a: Cls) -> None:
        pass

    class Cls:
        pass

    ann = annotationlib.get_annotations(func, format=annotationlib.Format.VALUE)
    assert ann["a"] is Cls
    assert ann["return"] is type(None)
else:
    # annotationlib ships in 3.14+; example validated on 3.14 interpreters
    assert sys.version_info.major == 3
```

---

## Supporting APIs

| Function | Role |
|----------|------|
| `get_annotate_from_class_namespace(ns)` | Retrieve `__annotate__` from class dict |
| `call_annotate_function(fn, format, …)` | Invoke annotate callable directly |
| `call_evaluate_function(fn, …)` | Run evaluate hooks |
| `ForwardRef` | Proxy for unresolved forward references in `FORWARDREF` format |

See also [Using annotations in a metaclass](https://docs.python.org/3/library/annotationlib.html#using-annotations-in-a-metaclass) and [custom callable annotate functions](https://docs.python.org/3/library/annotationlib.html#creating-a-custom-callable-annotate-function).

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`get_annotations`** instead of raw `obj.__annotations__` | Handles descriptors and deferred evaluation |
| Pick **`Format.STRING`** for doc generators | No code execution |
| Pick **`Format.FORWARDREF`** for static analysis tools | Safe unresolved names |
| Read [Annotations Best Practices](https://docs.python.org/3/howto/annotations.html) | Cross-version guidance |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `VALUE` on undefined forward refs | `NameError` | Use `FORWARDREF` or define names first |
| Executing annotations from untrusted modules | Arbitrary code | Sandbox or stick to `STRING` format |
| Mixing PEP 563 strings with 3.14 defaults | Double indirection | Standardize per package |

---

## See also

- [`__future__`](../__future__-future-statement-definitions/index.md) — legacy stringified annotations
- [`inspect`](../inspect-inspect-live-objects/index.md) — general callable introspection
- [PEP 649](https://peps.python.org/pep-0649/) / [PEP 749](https://peps.python.org/pep-0749/)
