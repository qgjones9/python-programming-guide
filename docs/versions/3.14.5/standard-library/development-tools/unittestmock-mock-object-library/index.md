# [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html)

`unittest.mock` provides **test doubles**: objects that record calls, return configured values, and replace dependencies during tests. **`Mock`**, **`MagicMock`**, **`patch`**, and **`create_autospec`** are the everyday tools. Canonical reference: [unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html).

---

## Purpose

Use mocks to **isolate** the unit under test from slow or non-deterministic collaborators (network, filesystem, clock). Patch where an object is **looked up** (`target`'s namespace), not where it is defined.

---

## Key types and functions

| Name | Role |
|------|------|
| `Mock` / `MagicMock` | Generic callable objects with automatic child mocks |
| `patch(target, new=...)` | Context manager / decorator replacing an attribute |
| `patch.object(obj, name)` | Patch attribute on a specific instance or class |
| `create_autospec(real)` | Mock with signature matching `real` |
| `call`, `ANY`, `sentinel` | Call comparison helpers |
| `AsyncMock` | Awaitable mocks for asyncio code |

---

## Example — Mock return values and call assertions

```python
from unittest.mock import Mock

service = Mock()
service.fetch.return_value = {"status": "ok"}

data = service.fetch("users")
assert data["status"] == "ok"
service.fetch.assert_called_once_with("users")
```

---

## Example — patch where used

```python
import urllib.request
from unittest.mock import patch, MagicMock

def get_title(url: str) -> str:
    with urllib.request.urlopen(url) as resp:
        return resp.read(5).decode()

fake_resp = MagicMock()
fake_resp.__enter__.return_value.read.return_value = b"Hello"

with patch("urllib.request.urlopen", return_value=fake_resp):
    assert get_title("http://example") == "Hello"
```

---

## Example — autospec enforces interface

```python
from unittest.mock import create_autospec

class Repository:
    def save(self, item: dict) -> bool:
        return True

repo = create_autospec(Repository, instance=True)
repo.save({"id": 1})
repo.save.assert_called_once_with({"id": 1})
```

---

## Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Patching wrong import path | Patch `pkg.module.func` as imported in the module under test |
| `Mock()` accepts any attribute call | Use `spec` or `autospec` to catch typos |
| Forgetting `return_value` on child mocks | Access creates auto-mocks; configure explicitly |
| `@patch` argument order | Patches apply bottom-up; mock params reverse decorator order |

---

## See also

- [Getting started guide](unittestmock-getting-started/index.md)
- [`unittest`](unittest-unit-testing-framework/index.md)
