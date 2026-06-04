# [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)

A **`def` statement** binds a name to a **function object** wrapping the suite. The body runs only on **call**; decorators run at **definition** time. Parameters support defaults, `/` positional-only, `*` keyword-only, `*args` / `**kwargs`, [annotations](../annotations/index.md), and [type parameter lists](../type-parameter-lists/index.md). Call semantics: [Calls](../../expressions/index.md). Reference: [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#function-definitions).

Parent: [Compound statements](../index.md)

---

## Definition-time vs call-time

| Aspect | When it happens |
|--------|-----------------|
| Decorator expressions | Function definition (outer scope) |
| Default parameter expressions | Once at definition |
| Annotations (3.14+ default) | Lazy; stored for later evaluation |
| Function body suite | Each call |
| `global` / `nonlocal` in body | Affect name resolution in nested defs |

```ebnf
funcdef ::= [decorators] "def" funcname [type_params] "(" [parameter_list] ")"
            ["->" expression] ":" suite
```

---

## Parameter forms

| Syntax | Role |
|--------|------|
| `name` | Positional or keyword (unless `/` or `*` rules apply) |
| `name=expr` | Default if argument omitted |
| `name: annotation` | Annotation only; see [Annotations](../annotations/index.md) |
| `/` | Parameters before `/` are positional-only |
| `*` | Starts keyword-only section |
| `*name` | Var-positional tuple |
| `**name` | Var-keyword mapping |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use `None` default + fresh mutable in body | Defaults evaluated once; shared list/dict bug |
| Apply `@functools.wraps` on decorators | Preserves metadata and `__wrapped__` |
| Put `/` on APIs that must not accept keyword args | Stable C-accelerated or protocol boundaries |
| Keep decorators simple at definition time | Heavy work belongs inside the wrapper |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Mutable default `def f(x=[])` | Shared across calls | `x=None` pattern |
| Decorator order | `@a @b` → `a(b(f))` | Read bottom-up application |
| Annotation forward refs without strings | NameError at lazy eval time | Quote types or use `from __future__` (deprecated path) |
| Inner `def` capturing loop variable | Late binding surprises | Default arg trick or separate scope |

```python
# Goal: mutable default pitfall vs None guard
def bad_append(item, bucket=[]):
    bucket.append(item)
    return bucket


def good_append(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


assert bad_append(1) is bad_append(2)
assert good_append(1) is not good_append(2)
```

```python
# Goal: decorator application order and wraps metadata
import functools

def tag(label):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            return (label, fn(*a, **kw))
        return wrapper
    return deco


@tag("outer")
@tag("inner")
def greet(name):
    """Say hi."""
    return f"hi {name}"


assert greet.__name__ == "greet"
assert greet("Ada") == ("outer", ("inner", "hi Ada"))
```

```python
# Goal: positional-only parameter (PEP 570)
def slug(name, /, prefix="item"):
    return f"{prefix}:{name}"


assert slug("x") == "item:x"
assert slug("x", prefix="z") == "z:x"
```
