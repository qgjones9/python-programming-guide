# [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)

A **formatted string literal** (or **f-string**) is source code prefixed with `f` or `F`. Unlike ordinary string literals, an f-string is **not a fixed constant**: Python evaluates **replacement fields**—expressions inside `{…}`—at run time and inserts their values into the final `str`.

F-strings are the usual way to build readable, inline string output in modern Python: log lines, error messages, user-facing text, and quick debug output without calling `.format()` or `%` formatting.

## Version history

- **3.6** — f-strings added ([PEP 498](https://peps.python.org/pep-0498/))
- **3.7** — `await` and `async for` allowed inside replacement fields
- **3.8** — debug specifier `=` added
- **3.12** — [PEP 701](https://peps.python.org/pep-0701/) relaxed many lexical restrictions: nested strings, comments, and backslashes inside `{…}` are now permitted

## Basic syntax

Prefix the opening quote with `f`, then write expressions in curly braces:

```python
who = 'nobody'
nationality = 'Spanish'
f'{who.title()} expects the {nationality} Inquisition!'
# 'Nobody expects the Spanish Inquisition!'
```

Text outside `{…}` behaves like a normal string literal: [escape sequences](../escape-sequences/index.md) are processed (unless you also use the [raw prefix](../raw-string-literals/index.md)), and [triple-quoted](../triple-quoted-strings/index.md) f-strings can span lines.

To emit a literal `{` or `}` in the output, **double** the brace outside any replacement field:

```python
print(f'{{name}} = {42}')
# {name} = 42
```

## Replacement fields are real Python expressions

Each `{expression}` is evaluated **left to right** in the scope where the f-string appears. Rules worth remembering:

- **Empty `{}` is invalid** — there must be an expression inside.
- **Walrus (`:=`) and `lambda`** must be wrapped in parentheses inside the field.

```python
f'{(half := 1/2)}, {half * 42}'
# '0.5, 21.0'

f'{(lambda x: x * 2)(21)}'
# '42'
```

Since Python 3.12, a replacement field may contain nested strings—even using the **same quote type** as the outer f-string—and backslashes:

```python
a = dict(x=2)
f"abc {a["x"]} def"
# 'abc 2 def'

items = ["a", "b", "c"]
print(f"List contains:\n{"\n".join(items)}")
# List contains:
# a
# b
# c
```

Comments inside `{…}` run to the end of the physical line; the closing `}` may appear on a later line:

```python
a = 2
f"abc{a  # comment runs to end of this line
       + 3}"
# 'abc5'
```

## Combining with other prefixes

| Prefix | Meaning |
|--------|---------|
| `f'…'` | Formatted string |
| `rf'…'` / `fr'…'` | Raw f-string — backslashes outside `{…}` are literal; expressions still evaluate |
| `f'''…'''` | Multi-line f-string |

```python
name = 'Galahad'
favorite_color = 'blue'
f'{name}:\t{favorite_color}'
# 'Galahad:\tblue'

rf"C:\Users\{name}"
# 'C:\\Users\\Galahad'

f'''Three shall be the number of the counting
and the number of the counting shall be three.'''
```

See [String prefixes](../string-prefixes/index.md) for how `f` combines with `b`, `r`, and other letters.

## Field suffixes: debug, conversion, and format

After the expression, a replacement field may include:

| Suffix | Example | Effect |
|--------|---------|--------|
| **Debug** `=` | `{x=}` | Emits `name=value` (uses `!r` for the value) |
| **Conversion** `!s` / `!r` / `!a` | `{obj!r}` | Calls `str()`, `repr()`, or `ascii()` before formatting |
| **Format** `:` *spec* | `{n:10.2f}` | Passed to `format()` — width, precision, alignment, etc. |

```python
x = 42
f'{x=}'
# 'x=42'

number = 14.3
f'{number:20.7f}'
# '          14.3000000'
```

Full behavior is documented under [f-strings in the standard library](https://docs.python.org/3/library/stdtypes.html#f-strings) and the [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec).

### Dynamic format specifiers

Top-level format specs may embed **one level** of nested replacement fields (with optional conversion and format on the inner field):

```python
field_size = 20
precision = 7
number = 14.3

f'{number:{field_size}.{precision}f}'
# '          14.3000000'

f'{3:{field_size}}'
# '                   3'

f'{3:{field_size:05}}'
# '00000000000000000003'
```

Nested fields **cannot** contain another level of `{…}` inside their format spec.

## Nesting f-strings

An f-string may appear inside another f-string’s replacement field:

```python
name = 'world'
f'Repeated:{f" hello {name}" * 3}'
# 'Repeated: hello world hello world hello world'
```

Portable code should stay at **five or fewer** nesting levels. (CPython itself does not enforce this limit.)

## Docstrings

An f-string is **never** a docstring, even when it contains no `{…}` fields:

```python
def foo():
    f"Not a docstring"

foo.__doc__ is None  # True
```

Use a normal string literal for module, class, and function docstrings.

## Real-world uses

### Logging and observability

F-strings keep context on one line and defer string building until the log call runs:

```python
import logging

logger = logging.getLogger(__name__)

def process_order(order_id: str, items: int, total: float) -> None:
    logger.info(f'order {order_id}: {items} items, total ${total:.2f}')
```

Use `%`-style lazy logging only when profiling shows formatting cost matters; for most application code, f-strings are clearer.

### User-facing and API messages

Validation errors and HTTP responses benefit from inline interpolation:

```python
def validate_age(age: int) -> None:
    if age < 0:
        raise ValueError(f'age must be non-negative, got {age}')
    if age > 150:
        raise ValueError(f'age {age} is out of plausible range')

def not_found(resource: str, id: str) -> dict:
    return {'error': f'{resource} {id!r} not found'}
```

The `!r` conversion calls `repr()`, which adds quotes around strings—helpful in error text.

### Tables, reports, and aligned columns

Format specs replace manual padding and `str.format` boilerplate:

```python
rows = [('alice', 98.5), ('bob', 87.0)]
header = f"{'Name':<10} {'Score':>6}"
lines = [header, '-' * 17]
lines += [f'{name:<10} {score:6.1f}' for name, score in rows]
report = '\n'.join(lines)
```

### Quick debugging

The `=` debug specifier (3.8+) prints both the expression source and its value:

```python
user_id = 7
enabled = True
print(f'{user_id=} {enabled=}')
# user_id=7 enabled=True
```

Prefer this over temporary `print('user_id', user_id)` during development.

### SQL and templates (with care)

F-strings are **not** a substitute for parameterized queries. Never interpolate untrusted input into SQL or shell commands. Safe pattern: use f-strings only for **static** query skeletons or internal identifiers you control; pass user data via bound parameters:

```python
# OK: table name from a fixed allow-list
TABLES = {'users', 'orders'}
table = 'users'
assert table in TABLES
query = f'SELECT id, name FROM {table} WHERE id = ?'  # ? filled by DB-API

# Never: f"SELECT * FROM users WHERE name = '{user_input}'"
```

## Best practices

| Practice | Why |
|----------|-----|
| Prefer f-strings over `"%"` and `"{}".format()` for simple interpolation | Less noise; expressions sit next to the text they fill |
| Use format specs (`:>10`, `:.2f`, `:b`) for alignment and numeric display | Keeps formatting declarative in one place |
| Use `{var=}` while debugging | Shows name and value without repeating the identifier |
| Use `!r` in errors for values that might be confused (`''` vs `' '`) | `repr()` exposes type and quoting |
| Keep expressions in `{…}` short | Long logic belongs in variables or helpers above the f-string |
| Limit nesting depth | Deeply nested f-strings are hard to read and maintain |
| Do not use f-strings as docstrings | They are ignored by `__doc__` machinery |
| Never interpolate untrusted data into SQL, HTML, or shell commands | Use parameterized APIs and proper escapers |

## When *not* to use an f-string

- **Docstrings** — use plain `'…'` or `"""…"""`.
- **Static strings with no interpolation** — `f'hello'` adds noise; use `'hello'`.
- **Heavy internationalization** — gettext and similar systems expect format templates evaluated at translation time; f-strings embed expressions too early.
- **Logging hot paths at DEBUG level** — consider lazy `%` formatting if profiling shows wasted work when the level is disabled.
- **Complex templating** (HTML pages, email bodies) — use a template engine (`Jinja2`, etc.) for escaping and structure.
- **Building JSON or XML** — use `json.dumps()` or an XML library; f-strings do not escape structural characters.

## Related sections

| Section | Description |
|---------|-------------|
| [String prefixes](../string-prefixes/index.md) | How `f` combines with `r`, `b`, and other prefixes |
| [Raw string literals](../raw-string-literals/index.md) | Raw + formatted literals (`rf` / `fr`) |
| [Triple-quoted strings](../triple-quoted-strings/index.md) | Multi-line f-strings |
| [Escape sequences](../escape-sequences/index.md) | Backslash processing outside `{…}` |
| [Formal grammar for f-strings](../formal-grammar-for-f-strings/index.md) | BNF rules for f-string lexical structure |
| [t-strings](../t-strings/index.md) | Template string literals (`t` prefix, 3.14+) |

## See also

- [PEP 498 – Literal String Interpolation](https://peps.python.org/pep-0498/)
- [PEP 701 – Syntactic formalization of f-strings](https://peps.python.org/pep-0701/)
- [`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format) — related brace-based formatting on existing strings
- [f-strings (standard library)](https://docs.python.org/3/library/stdtypes.html#f-strings) — evaluation of debug, conversion, and format suffixes
