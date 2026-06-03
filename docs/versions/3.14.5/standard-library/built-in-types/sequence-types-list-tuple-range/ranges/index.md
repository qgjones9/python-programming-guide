# [Ranges](https://docs.python.org/3/library/stdtypes.html#ranges)

The `range` type represents an **immutable sequence of numbers**, most commonly used for iterating a fixed number of times in `for` loops.

---

## Range Construction

```python
class range(stop, /)
class range(start, stop, step=1, /)
```

- All arguments to `range()` must be integers (either built-in `int` or any object implementing `__index__()`).
- If `start` is omitted, it defaults to `0`.
- If `step` is omitted, it defaults to `1`.
- A `step` of `0` raises a `ValueError`.

### Sequence Definition

- **Positive step:**  
  The contents of a range `r` are defined by:  
  `r[i] = start + step*i` for `i >= 0` such that `r[i] < stop`.

- **Negative step:**  
  The same formula, but with the constraint `r[i] > stop`.

- If `r[0]` does not meet the above condition, the range object is empty.

- **Negative indices** are supported and work as with other sequences (indexing from the end).

- Ranges with absolute values larger than `sys.maxsize` are permitted, but some operations (like `len()`) may raise `OverflowError`.

---

## Examples

```python
list(range(10))                # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
list(range(1, 11))             # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
list(range(0, 30, 5))          # [0, 5, 10, 15, 20, 25]
list(range(0, 10, 3))          # [0, 3, 6, 9]
list(range(0, -10, -1))        # [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
list(range(0))                 # []
list(range(1, 0))              # []
```

---

## Features and Characteristics

- `range` objects implement **all common sequence operations** except concatenation and repetition (since ranges must represent a single arithmetic progression).
- The advantage of `range` over lists/tuples: **constant, minimal memory usage** regardless of the range's size (only stores `start`, `stop`, `step`).
- Ranges implement the [`collections.abc.Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence) ABC.  
- Support for:  
  - Containment tests (`in`)
  - Index lookup
  - Slicing
  - Negative indices

---

### Range Attributes

- `start`: Value of the start parameter (defaults to `0`)
- `stop`: Value of the stop parameter
- `step`: Value of the step parameter (defaults to `1`)

---

## More Examples

```python
r = range(0, 20, 2)
print(r)             # range(0, 20, 2)
print(11 in r)       # False
print(10 in r)       # True
print(r.index(10))   # 5
print(r[5])          # 10
print(r[:5])         # range(0, 10, 2)
print(r[-1])         # 18
```

---

### Equality and Comparison

- `==` and `!=` compare the **sequence of values**, not object identity.
    - Example: `range(0) == range(2, 1, 3)` is `True`
    - Example: `range(0, 3, 2) == range(0, 4, 2)` is `True`
    - The objects may have different `start`, `stop`, and `step`, but are equal if they yield the same sequence.

---

## Version Notes

- **Python 3.2:** 
  - Implemented the Sequence ABC
  - Added slicing and negative indices
  - Membership tests (`in`) for integers became constant-time
- **Python 3.3:** 
  - Equality and inequality (`==`, `!=`) test value sequences, not identities
  - Added `start`, `stop`, and `step` attributes

---

## See Also

- The [linspace recipe](https://docs.python.org/3/library/stdtypes.html#typesseq-range-linspace-recipe) shows how to implement a lazy range suitable for floating-point applications.