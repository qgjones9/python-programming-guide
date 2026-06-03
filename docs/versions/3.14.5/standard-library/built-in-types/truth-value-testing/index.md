# [Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)

Any Python object can be evaluated in a Boolean context—that is, you can use any value in an `if` or `while` condition, or as an operand to Boolean operators (`and`, `or`, `not`).

### Truth Value Rules

- **Default Behavior:**  
  By default, an object is considered *truthy* (counts as `True`) unless its class explicitly marks it as *falsy*. There are two main ways a class can make its instances be treated as `False`:
    - By defining a `__bool__()` method that returns `False`.
    - By defining a `__len__()` method that returns `0`.

  If either method is present and returns the expected value, it determines the object's "truthiness." If one of these methods raises an exception (for example, `NotImplemented`), Python propagates the exception and the object has no truth value (meaning it can't be tested for truth).

### Common "Falsy" Values

The following built-in objects are *falsy*—they evaluate as `False` in a Boolean context:

- **Constants explicitly set to be false:**  
  - `None`
  - `False`
- **Zero of any numeric type:**  
  - `0` (integer zero)
  - `0.0` (floating-point zero)
  - `0j` (complex zero)
  - `Decimal(0)` (decimal zero)
  - `Fraction(0, 1)` (fractional zero)
- **Empty sequences and collections:**  
  - `''` (empty string)
  - `()` (empty tuple)
  - `[]` (empty list)
  - `{}` (empty dictionary)
  - `set()` (empty set)
  - `range(0)` (empty range)

### Boolean Results from Operations

Operations and built-in functions that return a Boolean result will always return `False` (or `0`) for falsy values and `True` (or `1`) for truthy values—unless otherwise documented.

> **Note:** The Boolean operators `or` and `and` are special: they *return* one of their actual operands, not just `True` or `False`. This behavior is useful for idioms such as `x or default`.

---