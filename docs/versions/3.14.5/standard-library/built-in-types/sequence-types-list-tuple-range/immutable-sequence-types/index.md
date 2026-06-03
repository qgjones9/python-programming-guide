# [Immutable Sequence Types](https://docs.python.org/3/library/stdtypes.html#immutable-sequence-types)

A key feature of immutable sequence types—unlike mutable ones—is that they support the built-in `hash()` function, which allows them to be used as dictionary keys or stored in sets and frozensets.

For example:
```python
# Tuples (immutable) can be used as dictionary keys:
point = (2, 3)
positions = {point: "Top-right"}
print(positions[(2, 3)])  # Output: Top-right

# Tuples can also be added to sets:
unique_points = {(1, 2), (2, 3), (2, 3)}
print(unique_points)  # Output: {(1, 2), (2, 3)}
```

However, if an immutable sequence contains any unhashable elements (such as a list inside a tuple), attempting to hash it raises a `TypeError`:

```python
bad_tuple = (1, [2, 3])
hash(bad_tuple)  # Raises TypeError: unhashable type: 'list'
```
Only fully hashable (all elements hashable) immutable sequences can be used as dict keys or set elements.