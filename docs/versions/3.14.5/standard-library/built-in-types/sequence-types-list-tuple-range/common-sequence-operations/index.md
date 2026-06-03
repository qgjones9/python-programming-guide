# [Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)

Common sequence operations apply to nearly all built-in sequence types in Python—both mutable (like `list`) and immutable (like `tuple`, `str`, `range`). To help you implement custom sequence types, Python provides the `collections.abc.Sequence` abstract base class, which defines the standard interface.

Below is a summary table of typical sequence operations (here, `s` and `t` are sequences of the same type, `n`, `i`, `j`, `k` are integers, `x` is an arbitrary object):

| Operation          | Result / Meaning                                  | Notes     |
|--------------------|--------------------------------------------------|-----------|
| `x in s`           | `True` if any item of `s` equals `x`, else `False` | (1)       |
| `x not in s`       | `False` if any item of `s` equals `x`, else `True` | (1)       |
| `s + t`            | Concatenation of `s` and `t`                     | (6),(7)   |
| `s * n` or `n * s` | Sequence `s` repeated `n` times                  | (2),(7)   |
| `s[i]`             | The item at index `i` (0-based)                  | (3),(8)   |
| `s[i:j]`           | Slice from index `i` up to (but not including) `j` | (3),(4)   |
| `s[i:j:k]`         | Slice from `i` to `j` with step `k`              | (3),(5)   |
| `len(s)`           | Number of items in `s`                           |           |
| `min(s)`           | Smallest item in `s`                             |           |
| `max(s)`           | Largest item in `s`                              |           |

**Comparisons:**  
Sequences of the same type (like two lists or tuples) support equality and ordering: they are compared *lexicographically* by elements, and both their lengths and types must match for equality. See [Comparisons](../../comparisons/index.md) for details.

**Iteration and Mutation:**  
Iterators—forward or reversed—traverse sequences by index. For mutable sequences, even if contents change during iteration, the iterator advances the current index each time, stopping when an `IndexError` or `StopIteration` is raised (or, for reverse, when the index drops below zero).

---

### Notes & Key Behaviors

1. **Containment with `in`/`not in`:**  
   While generally used for checking if a single item exists, some sequences (like `str`, `bytes`, and `bytearray`) will accept *subsequences* as well:
   ```python
   "gg" in "eggs"  # True
   ```

2. **Sequence Repetition (`*`):**  
   If `n < 0`, the result is an empty sequence of the same type. Be careful: repeating a container like `[[]]` multiplies *references*, not values:
   ```python
   lists = [[]] * 3
   print(lists)          # [[], [], []]
   lists[0].append(3)
   print(lists)          # [[3], [3], [3]]
   # All elements refer to the same inner list—modifications affect all.
   # To create independent sub-lists:
   lists = [[] for _ in range(3)]
   lists[0].append(3)
   lists[1].append(5)
   lists[2].append(7)
   print(lists)          # [[3], [5], [7]]
   ```
   See the Python FAQ: [How do I create a multidimensional list?](https://docs.python.org/3/faq/programming.html#how-do-i-create-a-multidimensional-list).

3. **Indexing and Slicing:**  
   - Negative `i`/`j` are interpreted as `len(s) + i` or `len(s) + j` (so `s[-1]` is the last item).
   - For slices:  
     - If `i` is omitted/`None`, use `0`.
     - If `j` is omitted/`None`, use `len(s)`.
     - If `i` or `j` < `-len(s)`, use `0`.
     - If `i` or `j` > `len(s)`, use `len(s)`.
     - If `i >= j`, result is empty.
   - For extended slicing (`s[i:j:k]`): indices are `i, i+k, i+2*k, ...` up to but not including `j`; `k` may not be `0`. If omitted, `k` defaults to `1`.

4. **Concatenation (`+`) of Immutable Sequences:**  
   Concatenating (for example, with `+`) always makes a *new* object. Repeated concatenation is **quadratic** in cost for immutable types—prefer these approaches for efficiency:
   - **`str`**: gather pieces in a list, then `"".join(list)` or use `io.StringIO`.
   - **`bytes`**: use `b"".join(list)` or `io.BytesIO`, or build via a `bytearray`.
   - **`tuple`**: extend lists, then call `tuple(list)` at the end.
   - **Other types**: consult type-specific docs.
   - Types like `range` may not support `+` or `*` at all.

5. **IndexError:**  
   If `i` is out of range (not a valid index in `s`), Python raises `IndexError`.

---

### Sequence Methods

Sequence types further provide these methods:

- `sequence.count(value, /)`  
  Count occurrences of `value` in `sequence`.

- `sequence.index(value[, start[, stop]])`  
  Return index of the first occurrence of `value` in `sequence`.  
  Raises `ValueError` if `value` is not found.  
  Optional `start` and `stop` bounds limit the search to `sequence[start:stop]`—no data is copied internally.

> **Caution:** Not all sequence types accept `start` and `stop` for `index()`.

---
