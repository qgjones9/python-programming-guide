# [10. Full Grammar specification](https://docs.python.org/3/reference/grammar.html)

No sub-pages in this mirror; read [**10. Full Grammar specification**](https://docs.python.org/3/reference/grammar.html) on docs.python.org for the full grammar and commentary.

- Canonical: [10. Full Grammar specification](https://docs.python.org/3/reference/grammar.html)
- Cross-check wording with PEPs cited from that page when behavior evolved across releases.
- Standard library objects are specified in *[The Python Standard Library](https://docs.python.org/3/library/index.html)*, not necessarily here.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```
