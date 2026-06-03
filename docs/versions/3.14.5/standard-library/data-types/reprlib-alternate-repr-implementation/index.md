# [reprlib — Alternate repr() implementation](https://docs.python.org/3/library/reprlib.html)

The [`reprlib`](https://docs.python.org/3/library/reprlib.html) module produces **bounded-length object representations** for debuggers, logging, and custom `__repr__` implementations. The `Repr` class caps container lengths, string width, and recursion depth; `reprlib.repr()` uses the module singleton `aRepr`. The `@recursive_repr` decorator prevents infinite recursion in self-referential structures. Full attribute list is on [docs.python.org](https://docs.python.org/3/library/reprlib.html).

---

## Module-level API

| Name | Role |
|------|------|
| `repr(obj)` | Size-limited repr via `aRepr` |
| `aRepr` | Configurable `Repr` singleton |
| `@recursive_repr(fillvalue='...')` | Safe repr for recursive containers |

```python
# Goal: truncate long list in repr
import reprlib

big = list(range(100))
text = reprlib.repr(big)
assert "..." in text
assert len(text) < 200
```

---

## Repr configuration — [Repr Objects](https://docs.python.org/3/library/reprlib.html#repr-objects)

| Attribute | Default | Limits |
|-----------|---------|--------|
| `maxlevel` | 6 | Recursion depth |
| `maxlist`, `maxtuple`, `maxset`, … | 6 (dict 4) | Container item count |
| `maxstring` | 30 | String character count |
| `maxlong` | 40 | Integer digit count |
| `maxother` | 30 | Fallback type width |
| `fillvalue` | `'...'` | Recursion / truncation marker |
| `indent` | `None` | Multi-line indented output (3.12+) |

```python
# Goal: custom Repr with tighter dict limit
import reprlib

r = reprlib.Repr(maxdict=2, maxlevel=3)
sample = {"a": 1, "b": 2, "c": 3, "nested": {"x": [1, 2, 3]}}
text = r.repr(sample)
assert "..." in text
```

---

## recursive_repr decorator

Use on container `__repr__` methods that may include themselves.

```python
# Goal: list that contains itself prints safely
import reprlib

class Node(list):
    @reprlib.recursive_repr()
    def __repr__(self):
        return "<" + "|".join(reprlib.repr(x) for x in self) + ">"

n = Node([1, 2])
n.append(n)
text = repr(n)
assert "..." in text
assert text.startswith("<")
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Tune **`aRepr` globally** in app debug mode | One knob for all `reprlib.repr` calls |
| Subclass **`Repr`** for domain types | Custom `repr_TextIOWrapper`-style hooks |
| Use **`@recursive_repr`** on graph-like reprs | Prevents stack overflow |
| Set **`indent`** for multi-line debug logs | Easier diffing than one-liners |
| Keep limits **aggressive in production logs** | Prevents PII/blob blowups |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Truncated repr looks like full data | Silent loss of tail items | Log length + hash separately |
| **`maxstring` mangles escapes** | Shortened mid-escape sequence | Treat as diagnostic only |
| Forgetting decorator on recursive **`__repr__`** | RecursionError | `@recursive_repr` |
| Expecting **`reprlib.repr` == built-in `repr`** | Different limits | Pick one per context |
| Changing **`aRepr`** affects debugger | Global side effect | Restore or use local `Repr()` |

---

## See also

- [`pprint`](../pprint-data-pretty-printer/index.md) — layout-oriented pretty printing
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) — auto `__repr__` (not size-limited)
