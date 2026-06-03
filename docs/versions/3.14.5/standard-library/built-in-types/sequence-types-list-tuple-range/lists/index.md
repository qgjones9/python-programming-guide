# [Lists](https://docs.python.org/3/library/stdtypes.html#lists)


Lists are **mutable sequences** in Python, most commonly used to store collections of objects (often—but not always—of similar type).

---

## List Construction

A `list` can be created in several standard ways:

- **Empty list:**  
  ```python
  my_list = []
  ```

- **With initial items (comma-separated in brackets):**  
  ```python
  my_list = [a]
  my_list = [a, b, c]
  ```

- **List comprehensions:**  
  ```python
  squares = [x * x for x in iterable]
  ```

- **Using the constructor:**  
  ```python
  new_list = list()               # Empty list
  from_iterable = list(iterable)  # From an iterable object
  ```

The constructor copies elements from `iterable` into a new list, preserving order. If the argument is already a list, a shallow copy is returned (like `iterable[:]`).

Examples:
```python
list('abc')        # ['a', 'b', 'c']
list((1, 2, 3))    # [1, 2, 3]
list()             # []
```

Other Python operations—such as `sorted()`—also return lists.

> **Note:** Lists are generic containers in Python; they can hold items of any type.

---

## List Methods and Behavior

Lists implement all **common** and **mutable sequence operations**. They also offer additional specialized methods, including:

### `sort(*, key=None, reverse=False)`

Sorts the list *in-place* using the `<` operator for comparisons.

- This operation is **in-place**: the original list is modified (nothing is returned).
- If any comparison operation fails (raises an exception), the sort is stopped, and the list may be left partially modified.
- **Arguments** (must be specified as keywords):
  - `key`: a function that extracts a comparison value from each element (e.g., `key=str.lower`). If `None`, elements themselves are compared. Keys for elements are computed once per sort.
  - `reverse`: if `True`, sorts in descending (reverse) order.

Example:
```python
words = ['banana', 'Apple', 'cherry']
words.sort(key=str.lower, reverse=True)  # ['cherry', 'banana', 'Apple']
```

- The [`functools.cmp_to_key()`](https://docs.python.org/3/library/functools.html#functools.cmp_to_key) utility lets you convert a legacy comparison function to a `key`.

- The sort is **stable**: items that compare equal maintain their original order. This allows sorting on multiple keys in successive passes (e.g., department, then salary grade).

> For more examples and sorting practices, see [Sorting Techniques](https://docs.python.org/3/howto/sorting.html).

---

### Implementation Notes

- **CPython Detail:** While a list is being sorted, mutating (or sometimes even reading) the list is undefined behavior. The C implementation may make the list appear empty for the duration and raises `ValueError` if it detects mutation during a sort.

---

**See also:**  
For thread-safety details of list operations, refer to [Thread safety for list objects](https://docs.python.org/3/faq/library.html#thread-safety).