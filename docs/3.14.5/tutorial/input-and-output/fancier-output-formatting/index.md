# [Fancier Output Formatting](https://docs.python.org/3/tutorial/inputoutput.html#fancier-output-formatting)

Condensed notes for **§7.1** of [Input and Output](https://docs.python.org/3/tutorial/inputoutput.html): modern **f-strings**, **`str.format`**, legacy **`%`**, and manual building with **`str.rjust`**. For the full mini-language tables, follow the official page.

```python
# Alignment and fill live in the format spec after a colon inside `{...}`.
assert f"{'test':*>10}" == "******test"

# `format` method uses positional / named fields instead of f-string interpolation.
assert "{0} {1}".format("a", "b") == "a b"
```

## Sections in this repo

- [Formatted string literals](formatted-string-literals/index.md)
- [The String format() method](the-string-format-method/index.md)
- [Manual string formatting](manual-string-formatting/index.md)
- [Old string formatting](old-string-formatting/index.md)

Parent: [Input and Output](../index.md)
