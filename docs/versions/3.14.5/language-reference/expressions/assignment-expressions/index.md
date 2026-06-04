# [6.12. Assignment expressions](https://docs.python.org/3/reference/expressions.html#assignment-expressions)

The **walrus operator** `:=` binds a name and **returns** the expression value in one step (PEP 572, Python 3.8+):

```ebnf
assignment_expression: [identifier ":="] expression
```

Common patterns: capture a regex match or read chunks in a loop without a separate assignment statement.

```python
import re

data = "user: ada"
pattern = re.compile(r"user: (\w+)")
if match := pattern.search(data):
    assert match.group(1) == "ada"

# Simulate chunked reads without a real file.
chunks = ["abc", "def", ""]
collected = []
while chunk := (chunks.pop(0) if chunks else ""):
    collected.append(chunk)
assert collected == ["abc", "def"]
```

Parentheses are **required** when `:=` appears as a statement, in slices, lambdas, comprehensions, `assert`, `with`, and plain assignments. In `if` / `while` headers they are optional.

Parent: [6. Expressions](../index.md)
