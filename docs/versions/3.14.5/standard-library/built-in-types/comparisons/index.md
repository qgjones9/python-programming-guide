# [Comparisons](https://docs.python.org/3/library/stdtypes.html#comparisons)

Python provides **eight comparison operators** to test relations and equality between values. All of these comparisons have the same precedence (which is higher than Boolean operators like `and`, `or`, `not`). You can also **chain comparisons**—for example, `x < y <= z` is interpreted as `(x < y) and (y <= z)`, but `y` is only evaluated once and `z` isn’t evaluated if `x < y` is false.

Here’s a summary of the comparison operators with explanatory terms:

| Operator  | Meaning (Explanatory)         | Example                        |
|-----------|------------------------------|--------------------------------|
| `<`       | strictly less than           | `a < b` (Is a less than b?)    |
| `<=`      | less than or equal to        | `a <= b` (a is at most b?)     |
| `>`       | strictly greater than        | `a > b` (Is a greater than b?) |
| `>=`      | greater than or equal to     | `a >= b` (a is at least b?)    |
| `==`      | equal                        | `a == b` (a equals b?)         |
| `!=`      | not equal                    | `a != b` (a does not equal b?) |
| `is`      | object identity              | `a is b` (Are a and b the exact same object?) |
| `is not`  | negated object identity      | `a is not b` (Are a and b different objects?) |

> **Note:**  
> - Comparing values of *different types* generally returns `False` for equality (`==`) unless a type explicitly allows it.
> - The operators `<`, `<=`, `>`, and `>=` are only defined for objects where ordering is meaningful (e.g., they will raise a `TypeError` if used on complex numbers).
> - `==` is always defined; for many custom objects, it may behave like `is` unless the `__eq__()` method is defined.

### Example: Chained Comparisons and Custom Classes

```python
# Chained comparison: only one evaluation per variable
x, y, z = 1, 2, 3
print(x < y <= z)  # True
print(x < y and y <= z)  # True, same as above

# Overriding comparison in a custom class
class Number:
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        return isinstance(other, Number) and self.value == other.value
    def __lt__(self, other):
        return isinstance(other, Number) and self.value < other.value

a = Number(5)
b = Number(10)
print(a < b)   # True
print(a == b)  # False

# Object identity
d = [1, 2, 3]
e = d
f = [1, 2, 3]
print(d == f)      # True (values are equal)
print(d is f)      # False (not the same object)
print(d is e)      # True (same object in memory)
```

### Customization Rules

- If you want your custom class to be *orderable* (using `<`, `<=`, `>`, `>=`), implement the methods `__lt__()`, `__le__()`, `__gt__()`, and `__ge__()`; usually, `__lt__()` and `__eq__()` are enough for standard behavior.
- **Identity operators** (`is`, `is not`) always test if two variables refer to *the same object in memory*—their behavior **cannot be customized** and never raises exceptions.

### Additional Membership Operators

Python also supports `in` and `not in` to check if a value is present in a container—these require that the type be iterable or support the `__contains__()` method.

```python
colors = ["red", "green", "blue"]
print("red" in colors)      # True
print("yellow" not in colors) # True
```

**In summary:**  
Use comparison operators to test value relationships, equality, or object identity, and customize their behavior for your classes as needed for semantic correctness.
