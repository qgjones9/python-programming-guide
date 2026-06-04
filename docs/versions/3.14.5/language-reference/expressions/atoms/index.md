# [6.2. Atoms](https://docs.python.org/3/reference/expressions.html#atoms)

**Atoms** are the smallest syntactic units of expressions: names, literals, and forms wrapped in `()`, `[]`, or `{}`. The grammar:

```ebnf
atom: 'True' | 'False' | 'None' | '...' | identifier | literal | enclosure
```

### [6.2.1. Built-in constants](https://docs.python.org/3/reference/expressions.html#built-in-constants)

`True`, `False`, and `None` are keywords naming singleton constants. `...` (Ellipsis) is a token, not a keyword. These names cannot be reassigned.

```python
assert True is not False
assert None is not False
assert ... is Ellipsis
```

### [6.2.2. Identifiers (Names)](https://docs.python.org/3/reference/expressions.html#identifiers-names)

A bare name evaluates to the object bound in the current namespace; an unbound name raises `NameError`. See [Naming and binding](../../execution-model/naming-and-binding/index.md) for scope rules.

```python
value = 42
assert value == 42
```

#### [6.2.2.1. Private name mangling](https://docs.python.org/3/reference/expressions.html#private-name-mangling)

In a class body, identifiers starting with two or more underscores (and not ending with two or more) are rewritten to `_ClassName__name` before code generation.

```python
class Demo:
    __secret = "hidden"


assert Demo._Demo__secret == "hidden"
assert not hasattr(Demo, "__secret")
```

### [6.2.3. Literals](https://docs.python.org/3/reference/expressions.html#literals)

Literals denote immutable values (`int`, `float`, `complex`, `str`, `bytes`, templates). **Negative numbers** like `-3` are unary `-` applied to a positive literal, not a literal token.

#### [6.2.3.1. Literals and object identity](https://docs.python.org/3/reference/expressions.html#literals-and-object-identity)

Equal literal values may or may not share identity; do not use `is` to compare numeric literals.

```python
# Value equality is stable; identity of large ints is not guaranteed.
assert 7 == 7
big = 123456789
assert big == 123456789
```

#### [6.2.3.2. String literal concatenation](https://docs.python.org/3/reference/expressions.html#string-literal-concatenation)

Adjacent string or bytes literals concatenate at **compile time**:

```python
assert "hello" "world" == "helloworld"
assert b"a" b"b" == b"ab"
name = "Ada"
assert "Hello, " f"{name}!" == "Hello, Ada!"
```

### [6.2.4. Parenthesized forms](https://docs.python.org/3/reference/expressions.html#parenthesized-forms)

Parentheses group expressions. A **single** expression without a comma yields that expression; **two or more** comma-separated expressions yield a tuple. Empty `()` yields an empty tuple.

```python
assert (1) == 1          # not a tuple
assert (1,) == (1,)      # one-item tuple needs trailing comma
assert () == tuple()
assert (1, 2) == (1, 2)
```

### [6.2.5–6.2.8. Displays](https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries)

List, set, and dict **displays** build collections; comprehensions run in an implicit nested scope so loop targets do not leak.

```python
def doubled():
    return [x * 2 for x in range(3)]


assert doubled() == [0, 2, 4]
```

Use `{}` alone for an empty **dict**; empty sets require `set()`.

```python
empty_set = set()
assert empty_set == set()
assert type({}) is dict
```

Parent: [6. Expressions](../index.md)
