# [Mutable Sequence Types](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types)

The following table lists operations that apply specifically to mutable sequence types in Python. The [`collections.abc.MutableSequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableSequence) abstract base class facilitates correct implementation of these operations in custom types.

In this table:
- `s` is an instance of a mutable sequence type
- `t` is any iterable object
- `x` is an object whose type/value satisfies any constraints required by `s` (e.g., `bytearray` requires `0 <= x <= 255`)

| Operation        | Result / Effect                                                                      | Notes                 |
|------------------|-------------------------------------------------------------------------------------|-----------------------|
| `s[i] = x`       | Replace item at index `i` of `s` with `x`                                           |                       |
| `del s[i]`       | Remove item at index `i` from `s`                                                   |                       |
| `s[i:j] = t`     | Replace slice from `i` to `j` with the items from iterable `t`                      |                       |
| `del s[i:j]`     | Remove items in slice `i:j` (`s[i:j] = []`)                                         |                       |
| `s[i:j:k] = t`   | Replace items in slice `i:j:k` with those from `t`                                  | (1)                   |
| `del s[i:j:k]`   | Remove items in slice `i:j:k` from `s`                                              |                       |
| `s += t`         | Extend `s` by appending each element from `t` (`s[len(s):len(s)] = t`)              |                       |
| `s *= n`         | Update `s` by repeating its contents `n` times                                      | (2)                   |

#### Notes

1. If `k` (the step) is not equal to 1 in slice assignment, then `t` must have the *same length* as the slice being replaced.
2. The value `n` can be an integer or any object implementing `__index__()`. If `n` is zero or negative, the sequence is cleared. Items are not copied—multiple references may result, as with `s * n` in [Common Sequence Operations](../common-sequence-operations/index.md).


## Example use cases

```python
# Create a list
my_list = [1, 2, 3]

# Add an item to the end
my_list.append(4)
print(my_list)  # [1, 2, 3, 4]

# Remove an item by index
del my_list[1]
print(my_list)  # [1, 3]

# Replace a slice
my_list[1:3] = [5, 6]
print(my_list)  # [1, 5, 6]

# Extend by another sequence
my_list += [7, 8]
print(my_list)  # [1, 5, 6, 7, 8]

# Repeat contents
my_list *= 2
print(my_list)  # [1, 5, 6, 7, 8, 1, 5, 6, 7, 8]
```