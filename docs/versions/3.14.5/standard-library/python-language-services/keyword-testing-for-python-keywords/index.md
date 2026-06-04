# [keyword — Testing for Python keywords](https://docs.python.org/3/library/keyword.html)

The [`keyword`](https://docs.python.org/3/library/keyword.html) module lists **reserved identifiers** and **soft keywords** (context-sensitive words like `match` and `case`). Tokenizers and parsers use it to classify names without hard-coding grammar tables. Full lists and version notes remain on [docs.python.org](https://docs.python.org/3/library/keyword.html).

Related: [`token`](../token-constants-used-with-python-parse-trees/index.md) for `NAME` vs `SOFT_KEYWORD`; [`tokenize`](../tokenize-tokenizer-for-python-source/index.md) for the live token stream.

---

## Core API

| Name | Role |
|------|------|
| `keyword.kwlist` | Sorted list of hard keywords (`if`, `class`, `def`, …) |
| `keyword.iskeyword(s)` | `True` if `s` cannot be used as an identifier |
| `keyword.issoftkeyword(s)` | `True` for context-sensitive keywords (3.10+) |
| `keyword.softkwlist` | Sorted soft keywords (3.10+) |

```python
# Goal: distinguish keywords from valid identifiers
import keyword

assert keyword.iskeyword("class")
assert keyword.iskeyword("async")
assert not keyword.iskeyword("Class")
assert not keyword.iskeyword("my_var")
```

```python
# Goal: soft keywords are not hard keywords
import keyword

assert keyword.issoftkeyword("match")
assert keyword.issoftkeyword("case")
assert not keyword.iskeyword("match")  # valid as variable name outside match statement
assert "match" in keyword.softkwlist
```

---

## Hard vs soft keywords

| Category | Example | Identifier use |
|----------|---------|----------------|
| Hard keyword | `def`, `return`, `import` | Never allowed as bare name |
| Soft keyword | `match`, `case`, `_` (pattern) | Allowed when grammar does not expect the keyword form |

Soft keywords let the language evolve new statement forms without breaking existing code that used the same spelling as a variable.

```python
# Goal: validate a user-chosen attribute name
import keyword

def safe_identifier(name: str) -> bool:
    return name.isidentifier() and not keyword.iskeyword(name)

assert safe_identifier("payload")
assert not safe_identifier("for")
assert safe_identifier("match")  # hard keyword check only; soft keywords may still be names
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`iskeyword`** before generating Python source | Avoid `SyntaxError` in codegen |
| Check **`issoftkeyword`** when writing pattern-match-aware tools | Token type may be `SOFT_KEYWORD` in `tokenize` output |
| Do not cache **`kwlist`** across interpreter upgrades | New releases add keywords (`type`, `match`, …) |

---

## See also

- [`token`](../token-constants-used-with-python-parse-trees/index.md) — `SOFT_KEYWORD` constant
- [`ast`](../ast-abstract-syntax-trees/index.md) — grammar constructs built from keywords
