# [The match statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

**Structural pattern matching** (3.10+) compares a **subject** (`match` expression) against **`case` patterns** in order. The first pattern that succeeds and whose optional **`if` guard** is true runs its suite; later cases are skipped. `match` and `case` are **soft keywords**. Full pattern algebra: [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement) (PEP 634 / 636).

Parent: [Compound statements](../index.md)

---

## Control flow

| Stage | Behavior |
|-------|----------|
| Subject evaluation | Comma in subject builds a tuple (standard rules) |
| Pattern attempt | Per `case`, top to bottom |
| Guard | `if assignment_expression`; evaluated only after pattern success |
| Bindings | Names bound in successful pattern are visible in the case suite |
| Irrefutable case | Catch-all (e.g. `case _:`) without guard; at most one, must be last |

Do **not** rely on bindings or side effects from **failed** matches — implementations may optimize evaluation.

---

## Pattern families (quick reference)

| Pattern | Idea |
|---------|------|
| Literal | `==` (or `is` for `None` / `True` / `False`) |
| Capture `name` | Always succeeds; binds subject |
| `_` | Wildcard; matches, binds nothing |
| Sequence `[a, b]` | Length and element-wise match |
| Mapping `{k: v}` | Keys present; subpatterns on values |
| Class `Cls(x, y=pat)` | `isinstance` + attribute / `__match_args__` |
| `P1 \| P2` | OR; same names in all branches |

---

## Best practices

| Practice | Why |
|----------|-----|
| Put specific cases before general ones | First match wins |
| Use guards for extra conditions, not complex patterns | Guards run only after structural match |
| End with `case _:` when exhaustiveness matters | Documents intentional default |
| Prefer `match` for destructuring, not arbitrary logic | `if`/`elif` stays clearer for simple booleans |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Class pattern without `__match_args__` | Positional args need keyword mapping | Define `__match_args__` or use keywords only |
| Duplicate capture names in one pattern | SyntaxError | Rename or use OR with consistent names |
| Guard with side effects | Order-dependent | Keep guards pure when possible |
| Using `_` as subject name | `_` is wildcard only inside patterns | Ordinary identifier in `match` subject |

```python
# Goal: first matching case wins; guard filters success
def classify(point, require_positive):
    match point:
        case (0, 0):
            return "origin"
        case (x, y) if require_positive and x > 0 and y > 0:
            return "positive-quadrant"
        case (x, y):
            return f"point-{x}-{y}"


assert classify((0, 0), False) == "origin"
assert classify((1, 2), True) == "positive-quadrant"
assert classify((-1, 2), True) == "point--1-2"
```

```python
# Goal: mapping pattern binds values
def http_label(status):
    match status:
        case {"code": 404}:
            return "not-found"
        case {"code": code} if 500 <= code < 600:
            return "server-error"
        case {"code": code}:
            return f"code-{code}"


assert http_label({"code": 404}) == "not-found"
assert http_label({"code": 503}) == "server-error"
```
