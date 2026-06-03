# [Boolean Type - bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)

The `bool` type represents truth values in Python and has exactly two constants: `True` and `False`.

```python
a = True
b = False
print(type(a))  # <class 'bool'>
```

### Creating Booleans

Use the built-in `bool()` function to convert any value to its boolean equivalent (see "Truth Value Testing"):

```python
bool(0)        # False
bool(42)       # True
bool([])       # False
bool([1, 2, 3]) # True
bool('hello')  # True
bool('')       # False
```

### Logical Operations

Use the logical operators `and`, `or`, and `not` for combining and inverting booleans:

```python
x = True
y = False

print(x and y)  # False
print(x or y)   # True
print(not x)    # False
```

### Bitwise Operators on Booleans

You can use the bitwise operators `&`, `|`, and `^` with booleans, which behave equivalently to logical **AND**, **OR**, and **XOR**:

```python
a = True
b = False

print(a & b)    # False (same as a and b)
print(a | b)    # True  (same as a or b)
print(a ^ b)    # True  (exclusive or)
```

> **Note:** Prefer `and`, `or`, and `!=` over `&`, `|`, and `^` for boolean logic.

**Deprecated since version 3.12:**  
The bitwise inversion operator `~` is deprecated for booleans and will raise an error in Python 3.16:

```python
~True   # Deprecated: Don't use this (was -2)
```

### Booleans as Integers

`bool` is a subclass of `int`. In numeric contexts, `False` behaves as `0` and `True` as `1`, but it is recommended to convert explicitly using `int()`:

```python
True + True    # 2
int(False)     # 0
int(True)      # 1

# Discouraged: Don't rely on automatic conversion in expressions
n_items = True * 10   # 10
# Prefer explicit conversion:
n_items = int(True) * 10  # 10
```

> See [Numeric Types — int, float, complex](../numeric-types-int-float-complex/index.md) for details.