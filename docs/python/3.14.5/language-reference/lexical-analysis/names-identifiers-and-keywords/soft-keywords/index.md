# [Soft Keywords](https://docs.python.org/3/reference/lexical_analysis.html#soft-keywords)

> **New in version 3.10**

Some names are treated as reserved **only in certain syntactic contexts**—these are called **soft keywords**. Unlike regular keywords, soft keywords can be used as ordinary identifiers except when the grammar specifically requires them as keywords.

- `match`, `case`, and `_` act as keywords only within a `match` statement.
- `type` acts as a keyword only within the `type` statement.

This context-sensitive treatment is handled at the parser level rather than the tokenizer, allowing these names to remain valid as identifiers elsewhere in code, preserving backward compatibility with existing programs.

> **Changed in version 3.12:**  
> `type` became a soft keyword.


## Examples: Using Soft Keywords as Identifiers and as Keywords

Here are examples demonstrating the correct and incorrect usage of **soft keywords** in Python:

### 1. Using `match`, `case`, and `_` in Different Contexts

Soft keywords like `match` and `case` are only treated as keywords within a `match` statement (introduced in Python 3.10+).

#### ✅ Correct Usage: Using as Identifiers Outside Their Keyword Context

```python
match = "pattern matching is cool"   # OK: variable named 'match'
case = 42                            # OK: variable named 'case'
_ = "wildcard variable"              # OK: '_' can be used as an ordinary name

print(match, case, _)
```

#### ✅ Correct Usage: Using as Keywords in a Match Statement

```python
value = 10
match value:
    case 10:
        print("Matched 10")
    case _:
        print("Wildcard match")
```

#### ❌ Incorrect Usage: Syntax Errors with True Keywords (for comparison)

```python
def = 5      # ❌ SyntaxError: 'def' is a reserved keyword

class = "foo"  # ❌ SyntaxError: 'class' is a reserved keyword
```

### 2. Soft Keyword `type` (Python 3.12+)

Starting in Python 3.12, `type` is a soft keyword only inside the new [type statement](https://docs.python.org/3/whatsnew/3.12.html#pep-695) context.

#### ✅ Correct Usage: `type` as an Identifier

```python
type = "This is just a variable"
print(type)  # OK
```

#### ✅ Correct Usage: `type` as a Soft Keyword (in a type statement, Python 3.12+)

```python
# PEP 695: Type Parameter Syntax (Python 3.12+)
type Stack[T] = list[T]

s: Stack[int] = [1, 2, 3]
```

#### ❌ Incorrect Usage: Syntax Error with Soft Keyword Used Incorrectly

```python
# The following would fail prior to Python 3.12 (since 'type' wasn't a statement)
type Foo = int   # ❌ SyntaxError in Python <3.12
```

### 3. Interaction with Reserved Keywords

Remember, soft keywords **can** be used as identifiers outside their special syntactic roles,
while true keywords **cannot**:

```python
if = 1  # ❌ SyntaxError: 'if' is a reserved keyword and cannot be used as a variable name
```

### Summary Table

| Soft Keyword | OK as Identifier? | Becomes Keyword In...     |
|--------------|:-----------------:|--------------------------|
| match        |       ✅          | `match` statement        |
| case         |       ✅          | `match` statement        |
| _ (underscore) |    ✅          | `match` pattern matching |
| type         |       ✅          | `type` statement (3.12+) |

> Use soft keywords freely as identifiers, except when Python expects them as keywords in specific grammar constructs.

