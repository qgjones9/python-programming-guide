# [The if statement](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)

The **`if` statement** selects **exactly one** suite to run: Python evaluates each `if` / `elif` condition in order until one is [true](../../expressions/boolean-operations/index.md), executes that suite, and skips the rest. If every condition is false and an `else` clause exists, the `else` suite runs. Full grammar and the “dangling else” rules are on [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement).

Parent: [Compound statements](../index.md)

---

## Grammar and evaluation

| Piece | Role |
|-------|------|
| `if assignment_expression :` | First test; may use walrus `:=` in the condition |
| `elif assignment_expression :` | Further tests, same rules as `if` |
| `else :` | Runs only when no earlier condition was true |
| **Suite** | Block executed for the first true branch only |

```ebnf
if_stmt ::= "if" assignment_expression ":" suite
            ("elif" assignment_expression ":" suite)*
            ["else" ":" suite]
```

Conditions use the same truth-value rules as `while` and `and` / `or`: falsy values include `0`, empty containers, `None`, and `False`.

---

## Best practices

| Practice | Why |
|----------|-----|
| Order `elif` from most specific to general | First match wins; broader tests hide later branches |
| Use `elif` instead of nested `if` when branches are mutually exclusive | Clearer intent and correct `else` binding |
| Keep conditions simple; assign in the header with `:=` when it helps readability | Walrus is allowed in `assignment_expression` |
| Prefer early `return`/`continue` in functions over deep nesting | Reduces indentation and dangling-else risk |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| One-line `if` with `;` and inner `if` | `else` attaches to the nearest `if` | Indent nested branches |
| Truthiness surprises (`[]`, `0`, `""`) | Empty data skips the “happy path” | Compare explicitly (`is None`, `len`, `==`) |
| Side effects in conditions | Runs only until first true branch | Do not rely on every branch being evaluated |
| Using `if` for value selection | Verbose vs `x if cond else y` | Ternary for expressions; `if` for statements |

```python
# Goal: first true branch wins; else runs when all tests fail
def sign_label(n):
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    else:
        return "positive"


assert sign_label(-3) == "negative"
assert sign_label(0) == "zero"
assert sign_label(7) == "positive"
```

```python
# Goal: walrus in if header avoids double lookup
data = {"items": [1, 2, 3]}
if (n := len(data.get("items", []))) > 2:
    result = f"many ({n})"
else:
    result = f"few ({n})"
assert result == "many (3)"
```
