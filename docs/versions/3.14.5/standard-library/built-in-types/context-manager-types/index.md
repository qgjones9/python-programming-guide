# [Context Manager Types](https://docs.python.org/3/library/stdtypes.html#context-manager-types)

The **`with`** statement runs a block inside a **runtime context** managed by a **context manager**. Any object implementing **`__enter__`** and **`__exit__`** can serve as a context manager. Full specification remains on [docs.python.org](https://docs.python.org/3/library/stdtypes.html#context-manager-types); this page explains the protocol and how it fits everyday code.

---

## Role of context managers in Python programs

Context managers centralize **setup** and **teardown** so callers cannot forget cleanup—even when an exception occurs.

| Use case | Built-in example |
|----------|------------------|
| Close files promptly | `with open(path) as f:` |
| Acquire/release locks | `threading.Lock` |
| Temporary decimal precision | `decimal.localcontext()` |
| Redirect stdout / suppress output | [`contextlib`](https://docs.python.org/3/library/contextlib.html) helpers |

Python does not treat these types specially in the interpreter beyond implementing the **context management protocol**. See the [**`contextlib`**](https://docs.python.org/3/library/contextlib.html) module for utilities such as [`contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager), [`closing`](https://docs.python.org/3/library/contextlib.html#contextlib.closing), and [`suppress`](https://docs.python.org/3/library/contextlib.html#contextlib.suppress).

---

## The context management protocol

A **`with`** statement evaluates the context expression, calls **`__enter__()`**, runs the suite, then **always** calls **`__exit__()`**—even if the suite raised an exception.

```python
import io

with io.StringIO('hello') as stream:
    text = stream.read()
assert text == 'hello'
```

| Phase | Method | Purpose |
|-------|--------|---------|
| Enter | [`__enter__()`](#contextmanager__enter__) | Prepare resources; optional value for `as` target |
| Body | *(suite)* | User code runs here |
| Exit | [`__exit__(exc_type, exc_val, exc_tb)`](#contextmanager__exit__) | Tear down; optionally suppress exceptions |

---

## [`__enter__()`](https://docs.python.org/3/library/stdtypes.html#context-manager-types)

<a id="contextmanager__enter__"></a>

### `contextmanager.__enter__()`

Enter the runtime context. Return **`self`** or another object bound to the name in an **`as`** clause:

```python
with open(__file__) as f:  # file returns itself
    assert f.readable()
```

| Return value | Example | Why |
|--------------|---------|-----|
| **`self`** | File objects from **`open()`** | Call methods on the open file inside the block |
| **Related object** | **`decimal.localcontext()`** | Expose a *copy* of thread-local state to mutate safely |

```python
from decimal import Decimal, localcontext, Context

with localcontext(Context(prec=2)) as ctx:
    assert ctx.prec == 2
    q = (Decimal('1') / Decimal('3')).quantize(Decimal('0.01'))
    assert q == Decimal('0.33')
```

Changes made to the **`localcontext()`** copy inside the block do not affect the decimal context outside it.

---

## [`__exit__(exc_type, exc_val, exc_tb)`](https://docs.python.org/3/library/stdtypes.html#context-manager-types)

<a id="contextmanager__exit__"></a>

### `contextmanager.__exit__(exc_type, exc_val, exc_tb)`

Exit the runtime context. Return a **Boolean** indicating whether to **suppress** an exception raised in the **`with`** body.

| Argument | When exception occurred | When no exception |
|----------|-------------------------|-------------------|
| **`exc_type`** | Exception class | `None` |
| **`exc_val`** | Exception instance | `None` |
| **`exc_tb`** | Traceback object | `None` |

**Return value:**

| Return | Effect |
|--------|--------|
| **`True`** (or any truthy value) | Suppress the exception; execution continues after **`with`** |
| **`False`** / **`None`** | Re-raise the exception after **`__exit__`** completes |

!!! note
    Do **not** re-raise the passed-in exception from **`__exit__`**. Return **`False`** to propagate it. If **`__exit__`** itself raises, that new exception is raised and the original is stored in its **`__context__`** attribute.

```python
class SuppressValueError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is ValueError

with SuppressValueError():
    raise ValueError('handled inside __exit__')

completed = True
assert completed
```

```python
class NeverSuppress:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

try:
    with NeverSuppress():
        raise RuntimeError('propagate')
except RuntimeError as err:
    assert str(err) == 'propagate'
```

---

## Implementing context managers

### Class-based protocol

Define **`__enter__`** and **`__exit__`** on the class:

```python
class Tag:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

with Tag() as tag:
    assert isinstance(tag, Tag)
```

### Generator-based (`contextlib.contextmanager`)

A generator function decorated with **`@contextlib.contextmanager`** yields once; code **before** **`yield`** runs on enter, code **after** **`yield`** (typically in **`finally`**) runs on exit. The decorator supplies **`__enter__`** / **`__exit__`** automatically.

```python
from contextlib import contextmanager

@contextmanager
def managed():
    state = ['enter']
    try:
        yield state
    finally:
        state.append('exit')

with managed() as state:
    state.append('body')
assert state == ['enter', 'body', 'exit']
```

---

## C API note

There is **no dedicated slot** for **`__enter__`** or **`__exit__`** in the Python/C API type structure. Extension types expose these as ordinary Python-callable methods; lookup cost is negligible compared to setting up the runtime context.

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Built-in Types](../index.md) | Overview of standard interpreter types including files and locks that implement this protocol. |
| [Mapping Types — dict](../mapping-types-dict/index.md) | Dicts are not context managers; contrast resource lifecycle with mapping access patterns. |

**See also:** [**`contextlib`**](https://docs.python.org/3/library/contextlib.html) — `@contextmanager`, `AbstractContextManager`, `ExitStack`, and helpers for writing and composing managers.
