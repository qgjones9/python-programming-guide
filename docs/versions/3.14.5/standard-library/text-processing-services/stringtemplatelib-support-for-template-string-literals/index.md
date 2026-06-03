# [string.templatelib — Support for template string literals](https://docs.python.org/3/library/string.templatelib.html)

**Template strings (t-strings)**, added in Python 3.14, use a `t` prefix instead of `f` and produce a [`Template`](https://docs.python.org/3/library/string.templatelib.html#string.templatelib.Template) object rather than a finished `str`. Your code walks static `strings` and dynamic `interpolations` to implement SQL parameterization, HTML escaping, structured logging, or any domain-specific renderer. Full API details remain on [docs.python.org](https://docs.python.org/3/library/string.templatelib.html); see also [Template string literal syntax](https://docs.python.org/3/reference/lexical_analysis.html#template-string-literals) in the language reference.

---

## Template data model — [Template strings](https://docs.python.org/3/library/string.templatelib.html#template-strings)

A `Template` splits input into alternating literal text and interpolated values:

| Attribute | Role |
|-----------|------|
| `strings` | Tuple of literal segments (always one more element than `values`) |
| `interpolations` | Tuple of `Interpolation` objects (metadata + value) |
| `values` | Tuple of evaluated values (`tuple(i.value for i in interpolations)`) |

Adjacent interpolations insert an **empty string** into `strings`. Iteration yields non-empty literals and each `Interpolation` in order—**empty literals are skipped** when iterating.

```python
# Goal: build and inspect a Template via the constructor (works without t"..." syntax)
import importlib

def demo_template_model():
    try:
        tplib = importlib.import_module("string.templatelib")
    except ModuleNotFoundError:
        return  # module requires Python 3.14+
    Template = tplib.Template
    Interpolation = tplib.Interpolation
    cheese = "Camembert"
    template = Template(
        "Ah! We do have ",
        Interpolation(cheese, "cheese"),
        ".",
    )
    assert template.strings == ("Ah! We do have ", ".")
    assert template.values == ("Camembert",)
    assert len(template.strings) == len(template.values) + 1
    pieces = list(template)
    assert pieces[0] == "Ah! We do have "
    assert pieces[-1] == "."

demo_template_model()
```

With t-string literals (3.14+ interactive example):

```python
# Goal: t-string literal shape (requires Python 3.14+)
import importlib
import sys

if sys.version_info >= (3, 14):
    ns = {}
    exec(
        "from string.templatelib import Interpolation\n"
        "pi = 3.14\n"
        "tpl = t't-strings expose {pi!s} before rendering'\n"
        "assert isinstance(tpl.values[0], float)\n"
        "assert tpl.interpolations[0].conversion == 's'\n",
        ns,
        ns,
    )
```

---

## Interpolation objects — [Interpolation](https://docs.python.org/3/library/string.templatelib.html#string.templatelib.Interpolation)

Each `Interpolation` captures one `{...}` expression from the source (or manual construction):

| Attribute | Role |
|-----------|------|
| `value` | Evaluated Python object |
| `expression` | Source text inside `{...}` (excluding braces) |
| `conversion` | `None`, `'a'`, `'r'`, or `'s'` (like f-string `!a` / `!r` / `!s`) |
| `format_spec` | Text after `:` (not auto-applied—your renderer decides) |

Unlike f-strings, **conversions and format specs are not applied automatically**. Use [`convert()`](https://docs.python.org/3/library/string.templatelib.html#string.templatelib.convert) when you want f-string semantics.

```python
# Goal: apply f-string-style conversion in a custom renderer
import importlib

def render_with_conversions(template):
    tplib = importlib.import_module("string.templatelib")
    convert = tplib.convert
    parts = []
    for item in template:
        if isinstance(item, str):
            parts.append(item)
        else:
            converted = convert(item.value, item.conversion)
            if item.format_spec:
                parts.append(format(converted, item.format_spec))
            else:
                parts.append(str(converted))
    return "".join(parts)

try:
    tplib = importlib.import_module("string.templatelib")
except ModuleNotFoundError:
    pass
else:
    Template = tplib.Template
    Interpolation = tplib.Interpolation
    tpl = Template(
        "value=",
        Interpolation(3.0, "1. + 2.", None, ".2f"),
    )
    assert render_with_conversions(tpl) == "value=3.00"
```

---

## Combining templates

| Operation | Behavior |
|-----------|----------|
| `template + other` | Concatenates two `Template` instances |
| `template += other` | In-place concatenation |
| `Template + str` | **Not supported**—wrap the str in `Template(...)` or use `Interpolation` |

```python
# Goal: concatenate Template objects
import importlib

try:
    tplib = importlib.import_module("string.templatelib")
except ModuleNotFoundError:
    pass
else:
    Template = tplib.Template
    Interpolation = tplib.Interpolation
    left = Template("Hello, ")
    name = Interpolation("Ada", "name")
    right = Template(name, "!")
    combined = left + right
    assert "Hello, " in combined.strings[0]
    assert combined.values == ("Ada",)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Treat t-strings as **ASTs**, not strings | Prevents accidental injection when you control rendering |
| Apply `format_spec` in **one place** | Central policy for numbers, dates, and redaction |
| Use `convert()` for `!r` / `!s` / `!a` | Matches f-string coercion without building an f-string |
| Prefer literal `t"..."` at call sites | Constructor API is for library code assembling fragments |
| Do not concatenate raw `str` | Ambiguity between static and dynamic segments |

**Pitfall:** iterating skips empty literal segments—if you rely on positional indexing, use `strings` / `interpolations` tuples instead of `list(template)`.
