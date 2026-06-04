# [unittest.mock — getting started](https://docs.python.org/3/library/unittest.mock-examples.html)

This page walks through **common mocking patterns** from the official examples document: patching modules, autospec, side effects, and chaining. Full API details live in [`unittest.mock`](unittestmock-mock-object-library/index.md); canonical prose is at [unittest.mock-examples.html](https://docs.python.org/3/library/unittest.mock-examples.html).

---

## Patch a function in the module under test

Replace a collaborator at the **import site** so the code under test sees the mock.

```python
import datetime
from unittest.mock import patch

def is_weekend() -> bool:
    return datetime.datetime.today().weekday() >= 5

class FakeDate(datetime.datetime):
    @classmethod
    def today(cls):
        return cls(2024, 1, 6)  # Saturday

with patch("datetime.datetime", FakeDate):
    assert is_weekend() is True
```

---

## Side effects — exceptions and iterables

```python
from unittest.mock import Mock

m = Mock()
m.side_effect = [1, 2, ValueError("stop")]

assert m() == 1
assert m() == 2
try:
    m()
except ValueError as e:
    assert str(e) == "stop"
```

---

## Mock a context manager

```python
from unittest.mock import MagicMock

mgr = MagicMock()
mgr.__enter__.return_value = "inside"
mgr.__exit__.return_value = False

with mgr as value:
    assert value == "inside"
mgr.__enter__.assert_called_once()
```

---

## PropertyMock for `@property`

```python
from unittest.mock import patch, PropertyMock

class Config:
    @property
    def debug(self):
        return False

cfg = Config()
with patch.object(type(cfg), "debug", new_callable=PropertyMock) as mock_debug:
    mock_debug.return_value = True
    assert cfg.debug is True
```

---

## Tips from the official guide

| Pattern | When to use |
|---------|-------------|
| `patch.multiple` | Replace several names in one block |
| `wraps=` | Spy on real function while still calling it |
| `assert_called_with` vs `assert_called_once_with` | Distinguish repeated calls |
| `mock_open` | Stub `open()` for file I/O tests |

---

## See also

- [`unittest.mock` API reference](unittestmock-mock-object-library/index.md)
- [`unittest`](unittest-unit-testing-framework/index.md)
