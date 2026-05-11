# [Input and Output](https://docs.python.org/3/tutorial/inputoutput.html)

Condensed notes for [chapter 7 — Input and Output](https://docs.python.org/3/tutorial/inputoutput.html): **`str.format`**, **f-strings**, manual formatting, files, and **`json`** for structured data. For **`print`** details and binary modes, follow the official subsections.

### 7.1 — [Fancier Output Formatting](https://docs.python.org/3/tutorial/inputoutput.html#fancier-output-formatting)

- **F-strings** (`f"{expr=}"`) evaluate expressions at format time; **`str.format`** uses **`{0}` / `{name}`** placeholders with a mini-language for alignment, fill, and type conversion.

```python
name = "Ada"
# f-strings interpolate expressions inside `{...}` at runtime.
assert f"hi {name}" == "hi Ada"
assert f"{2 + 2=}" == "2 + 2=4"  # `=` debug syntax includes the expression text
```

### 7.2 — [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)

- **`open(path, mode, encoding=...)`** returns a context manager; text mode decodes bytes to **`str`** using **`encoding`** (UTF-8 default on modern platforms).

```python
import io

# `StringIO` mimics a text file object in memory — good for tests and tutorials.
buf = io.StringIO()
buf.write("line\n")
assert buf.getvalue() == "line\n"
```

### 7.3 — [Saving structured data with `json`](https://docs.python.org/3/tutorial/inputoutput.html#saving-structured-data-with-json)

- **`json.dumps` / `json.loads`** round-trip dicts/lists/strings/numbers/bools/`None`; keys must be strings on decode.

```python
import json

payload = {"ok": True, "count": 3}
text = json.dumps(payload)
assert json.loads(text) == payload
```

## Sections in this repo

- [Fancier Output Formatting](fancier-output-formatting/index.md)
- [Reading and Writing Files](reading-and-writing-files/index.md)

Next: [Errors and Exceptions](../errors-and-exceptions/index.md)
