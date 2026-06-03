# [Built-in Constants](https://docs.python.org/3/library/constants.html)

Python defines several **built-in constants** that are always available without needing to import any module. These represent special values, common singleton objects, or implementation details that are fundamental to the language. They are documented in the [official Python "Built-in Constants" reference](https://docs.python.org/3/library/constants.html).

## False

Represents the boolean value for "falsehood" in Python. It is a singleton instance of type `bool`.

```python
if False:
    print("This will not execute.")

assert isinstance(False, bool)
```

---

## True

Represents the boolean value for "truth" in Python. It is also a singleton instance of type `bool`.

```python
if True:
    print("This will always execute.")

assert isinstance(True, bool)
```

---

## None

The singleton object used to signify "the absence of a value" or "no result." Used as the default return for functions without a return statement.

```python
def no_return():
    pass

result = no_return()
assert result is None
```

---

## NotImplemented

A special return value that binary special methods (like `__eq__`, `__add__`) use to indicate that an operation is not supported with the given types. The interpreter will then try the reflected operation or report a `TypeError`.

```python
class OnlyAddInts:
    def __add__(self, other):
        if isinstance(other, int):
            return 42 + other
        return NotImplemented

assert (OnlyAddInts() + 5) == 47
try:
    OnlyAddInts() + "hello"
except TypeError:
    print("TypeError was raised")
```

---

## Ellipsis

The singleton object written as `...`. Most commonly used in advanced slicing (esp. NumPy arrays), but can also serve as a "to be implemented" marker.

```python
# As a placeholder
def todo_function():
    ... # used as a placeholder

def todo_function():
    pass # used as a placeholder

# ^ the ... is the same as pass in the above implementation

# As a slicing shortcut
slice_obj = (1, ..., 10)
print(slice_obj)  # Output: (1, Ellipsis, 10)
```

---

## __debug__

A special constant that is `True` under normal circumstances but becomes `False` when Python is started with the `-O` (optimize) flag. Used to control assertions and debug-only code.

```python
assert __debug__  # Usually True

def f(x):
    assert x > 0, "x must be positive (debug-only)"

# Run Python with -O (optimize) to remove assert statements and set __debug__ to False
```

Some interactive shells (such as the built-in REPL or IDLE) may also provide additional constants like `quit`, `exit`, `copyright`, `credits`, and `license`. These are added by the `site` module for convenience.

---

### Quick reference

| Constant         | Description                                                                                 |
|------------------|---------------------------------------------------------------------------------------------|
| `False`, `True`  | Boolean values for truth and falsehood (`bool` type singletons)                             |
| `None`           | The null object; identity of absence                                                        |
| `NotImplemented` | Special return value indicating an unsupported operation for binary special methods          |
| `Ellipsis`       | The `...` object; commonly used in advanced slicing and as a placeholder                    |
| `__debug__`      | Indicates if Python was started without -O optimization (`True` for normal mode)            |

---

For details on how these behave and can be used, see the individual sections for each constant in this directory.

- [Constants added by the site module](constants-added-by-the-site-module/index.md)
