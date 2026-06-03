# [Iterator Types](https://docs.python.org/3/library/stdtypes.html#iterator-types)

## The Iterator Protocol

Python enables iteration over container objects (like lists, tuples, dictionaries) using a standard protocol. Custom container types can also support iteration by implementing the appropriate special methods.

### Making an Object Iterable

To make an object iterable (usable in a `for` loop or with `iter()`):

- **`__iter__(self)`**
  - Should return an *iterator* object.
  - If the container supports multiple iteration orders/types, provide additional methods to request those iterators (e.g., breadth-first or depth-first).
  - Corresponds to the `tp_iter` slot in the Python/C API.

Example:

```python
class MyContainer:
    def __iter__(self):
        # Return an iterator object
        return MyIterator(self.data)
```

### The Iterator Object

An *iterator* object must implement both of these methods:

- **`__iter__(self)`**
  - Returns the iterator object itself (usually `return self`), allowing the object to be used in nested loops or with both `iter()` and `for`.

- **`__next__(self)`**
  - Returns the next value from the sequence.
  - Raises `StopIteration` when items are exhausted.

**Key property:**  
Once an iterator’s `__next__()` raises `StopIteration`, it must *always* continue to do so on subsequent calls—an exhausted iterator never "resets" itself.

Example custom iterator:

```python
class Counter:
    def __init__(self, limit):
        self.i = 0
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.limit:
            val = self.i
            self.i += 1
            return val
        else:
            raise StopIteration

c = Counter(3)
for x in c:
    print(x)  # 0, 1, 2
```

### Built-in and Specialized Iterators

Python provides many built-in iterator types:
- General: those from `iter()` on lists, dicts, ranges, etc.
- Specialized: e.g., dictionary keys, values, or items (`dict.keys()`, `dict.items()`).

As long as they meet the iterator protocol, the underlying types don't matter for normal code.

---

## Generator Types

A **generator** is a simple way to write iterators using a function with the `yield` keyword. Python treats a generator function as implementing both `__iter__()` (returns itself) and `__next__()` (runs until the next `yield` or raises `StopIteration`).

Example:

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for i in countdown(3):
    print(i)  # 3, 2, 1
```

See the [documentation for `yield`](https://docs.python.org/3/reference/expressions.html#yieldexpr) for more on generators.