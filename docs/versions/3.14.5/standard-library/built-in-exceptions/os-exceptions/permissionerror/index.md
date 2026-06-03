# [PermissionError](https://docs.python.org/3/library/exceptions.html#PermissionError)

`PermissionError` is raised when the process lacks rights to perform an operation on an **existing** resource—filesystem permissions, capability restrictions, or similar. It corresponds to `EACCES`, `EPERM`, and (on WASI) `ENOTCAPABLE`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#PermissionError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md).
- Distinct from [`FileNotFoundError`](../filenotfounderror/index.md) (path missing) and from authentication failures in application layers (often custom exceptions).

| errno constant | Typical meaning |
|----------------|-----------------|
| `EACCES` | Permission denied on access (read/write/execute bit). |
| `EPERM` | Operation not permitted (e.g. immutable flag, policy). |
| `ENOTCAPABLE` | WASI capability missing (mapped since 3.11.1). |

---

## When it is raised

Examples include writing a read-only file, executing a file without the execute bit, or crossing a directory boundary without search permission. The path usually **exists**; the kernel rejects the operation.

```python
import errno

def demo_permission_mapping():
    for code in (errno.EACCES, errno.EPERM):
        exc = OSError(code, "Permission denied", "/secret")
        assert isinstance(exc, PermissionError)
        assert exc.errno == code

demo_permission_mapping()
```

---

## Handling patterns

Do not confuse with “file not found” for security-sensitive paths—some systems hide existence behind permission errors. Treat the message as authoritative for users; log `errno` and `filename` for operators.

```python
import errno

def read_config(path):
    try:
        with open(path) as f:
            return f.read()
    except PermissionError as exc:
        raise RuntimeError(f"cannot read config {exc.filename!r}") from exc

# Demonstrate handler path via constructed exception
try:
    raise PermissionError(errno.EACCES, "denied", "/etc/shadow")
except PermissionError as exc:
    assert exc.strerror == "denied"
```

---

## Best practices

- Never silently ignore `PermissionError` in cleanup unless you document why (e.g. best-effort temp file removal).
- Fix the environment (chmod, user, container volume mounts) rather than catching broadly in library code.
- On Windows, also inspect `winerror` when present on the same `OSError` instance.
