# [LookupError](https://docs.python.org/3/library/exceptions.html#LookupError)

`LookupError` is the base class for failures when a **key** or **index** is not valid for a mapping or sequence. Built-in subclasses are [`KeyError`](../../concrete-exceptions/keyerror/index.md) and [`IndexError`](../../concrete-exceptions/indexerror/index.md). The standard library may also raise **`LookupError` itself**—for example when [`codecs.lookup()`](https://docs.python.org/3/library/codecs.html#codecs.lookup) cannot find an encoding. Full reference: [docs.python.org](https://docs.python.org/3/library/exceptions.html#LookupError).

---

## Role in the hierarchy

`LookupError` inherits from [`Exception`](../exception/index.md). Concrete lookup failures in user code almost always appear as `KeyError` or `IndexError`, but a handler for `LookupError` catches both.

```python
# Goal: KeyError and IndexError share LookupError
assert issubclass(KeyError, LookupError)
assert issubclass(IndexError, LookupError)
assert issubclass(LookupError, Exception)
```

---

## Subclasses and direct raises

| Type | Usually means |
|------|----------------|
| `KeyError` | Missing key on a `dict` or mapping (or `__getitem__` with no default) |
| `IndexError` | Sequence index out of range (after slice normalization) |
| `LookupError` (direct) | Codec name not found, or code raising the base intentionally |

```python
def safe_item(container, key_or_index, default=None):
    try:
        return container[key_or_index]
    except LookupError:
        return default

assert safe_item({}, "missing", 0) == 0
assert safe_item([10, 20], 99, 0) == 0
assert safe_item({"a": 1}, "a") == 1
```

### `codecs.lookup()`

Invalid encoding names raise **`LookupError`**, not `KeyError`:

```python
import codecs

def encoding_available(name):
    try:
        codecs.lookup(name)
        return True
    except LookupError:
        return False

assert encoding_available("utf-8") is True
assert encoding_available("not-a-real-encoding-name-xyz") is False
```

---

## Catching `LookupError` vs specific types

| Handler | Catches |
|---------|---------|
| `except KeyError` | Missing dict keys only |
| `except IndexError` | Bad sequence indices only |
| `except LookupError` | Both, plus direct `LookupError` (codecs, custom APIs) |

```python
def label_lookup_failure(exc):
    try:
        raise exc
    except KeyError:
        return "key"
    except IndexError:
        return "index"
    except LookupError:
        return "lookup"

assert label_lookup_failure(KeyError("x")) == "key"
assert label_lookup_failure(IndexError()) == "index"
assert label_lookup_failure(LookupError("codec")) == "lookup"
```

Put **more specific** handlers (`KeyError`, `IndexError`) **before** `LookupError` in the same `try`.

---

## When to use `LookupError`

| Use `LookupError` | Prefer `KeyError` or `IndexError` |
|-------------------|-----------------------------------|
| Function accepts either mappings or sequences | Type of container is known |
| Shared fallback for “identifier not found” | You re-raise with `from` to preserve type |
| Mirroring `codecs.lookup()` behavior | Public API should document exact failure |

For user-defined APIs, subclass `LookupError` only when callers truly need one handler for multiple lookup styles; otherwise subclass `KeyError`/`IndexError` or `Exception`.

---

## Best practices

- Use **`dict.get()`** or **`try` / `except KeyError`** deliberately—`get` avoids exceptions for missing keys.
- Remember **slice indices** are clamped silently; only integer indices that are out of range raise `IndexError`.
- When converting `KeyError` to another type, use **`raise NewError(...) from None`** or `from key_error` per [Exception context](../../exception-context/index.md).
- Do not catch `LookupError` when you only support mappings—catch `KeyError` for clearer diagnostics.

---

## Common pitfalls

- **`except LookupError` after `except Exception`** — unreachable; order matters.
- **`KeyError` message** is the key itself (since 3.x)—do not assume a human-readable sentence in `str(exc)`.
- Confusing **`LookupError`** with **`AttributeError`** for missing object attributes—use `getattr` defaults or `hasattr` patterns.
- **`UnicodeError`** hierarchy is separate—encoding **decode** failures are not `LookupError`.

---

## Sections in this repo

Concrete built-in types that inherit from `LookupError`:

| Type | Page |
|------|------|
| [KeyError](../../concrete-exceptions/keyerror/index.md) | Missing mapping keys |
| [IndexError](../../concrete-exceptions/indexerror/index.md) | Invalid sequence indices |

---

## Related pages

| Topic | Link |
|-------|------|
| Application error base | [Exception](../exception/index.md) |
| Parent index | [Base classes](../index.md) |
| Concrete exceptions list | [Concrete exceptions](../../concrete-exceptions/index.md) |
