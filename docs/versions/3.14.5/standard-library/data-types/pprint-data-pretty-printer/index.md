# [pprint — Data pretty printer](https://docs.python.org/3/library/pprint.html)

The [`pprint`](https://docs.python.org/3/library/pprint.html) module formats Python objects into **multi-line, indented representations** suitable for logs, REPL inspection, and doctest-style display. It handles nested dicts, lists, dataclasses (3.10+), and `SimpleNamespace` (3.9+). Output may not always be `eval`-able when objects are not literal-safe. Full `PrettyPrinter` API is on [docs.python.org](https://docs.python.org/3/library/pprint.html).

---

## Module functions

| Function | Role |
|----------|------|
| `pp(obj, …)` | Print formatted object + newline (3.8+); **`sort_dicts=False` default** |
| `pprint(obj, …)` | Alias with **`sort_dicts=True` default** |
| `pformat(obj, …)` | Return formatted string |
| `isreadable(obj)` | Could `eval` reconstruct value? |
| `isrecursive(obj)` | Needs recursion marker |
| `saferepr(obj)` | Bounded repr with recursion protection |

Common kwargs: `indent`, `width` (default 80), `depth`, `compact`, `underscore_numbers`.

```python
# Goal: readable nested structure as string
import pprint

data = {"users": [{"name": "Ada", "roles": ["admin", "dev"]}], "version": 2}
text = pprint.pformat(data, width=40, depth=2)
assert "users" in text
assert "..." in text or "Ada" in text
```

---

## PrettyPrinter objects — [PrettyPrinter Objects](https://docs.python.org/3/library/pprint.html#prettyprinter-objects)

| Method | Role |
|--------|------|
| `pprint(obj)` | Print to configured stream |
| `pformat(obj)` | Return string |
| `isreadable` / `isrecursive` | Same as module-level |
| `format(obj, context, maxlevels, level)` | Hook for subclasses |

Reuse a `PrettyPrinter` instance in hot logging loops to avoid re-parsing options.

```python
# Goal: cap depth to avoid dumping huge subgraphs
import pprint

nested = {"a": {"b": {"c": {"d": 1}}}}
printer = pprint.PrettyPrinter(depth=2)
out = printer.pformat(nested)
assert "..." in out
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`pp` in REPL** (`print = pprint.pp`) | Instant structure visibility |
| Set **`width`** to terminal/log column budget | Prevents horizontal scroll |
| Limit **`depth`** on unknown API payloads | Avoids leaking huge trees |
| Prefer **`sort_dicts=False`** when order matters | Insertion order visible in 3.7+ dicts |
| Combine with **`reprlib`** for size caps | Double protection in debug paths |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Assuming output is **`eval` safe** | Files, sockets, classes break | Use `isreadable` or JSON for data |
| Recursive structures | `<Recursion on list…>` markers | Expected — not a bug |
| **`pprint` vs `pp` sort defaults** | Keys reorder unexpectedly | Pick one function consistently |
| Logging secrets in **`pprint`** | Pretty still prints values | Redact before formatting |
| Very wide lines with `compact=False` | One item per line explosion | Enable `compact=True` |

---

## See also

- [`reprlib`](../reprlib-alternate-repr-implementation/index.md) — hard size limits
- [`json`](https://docs.python.org/3/library/json.html) — serializable pretty output
