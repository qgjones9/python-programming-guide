# [Audit events table](https://docs.python.org/3/library/audit_events.html)

Python's **audit hook** machinery fires events for security-sensitive operations: imports, compilation, socket creation, memory mapping, and more. Hook functions registered with [`sys.addaudithook`](https://docs.python.org/3/library/sys.html#sys.addaudithook) receive `(event, args)` pairs documented in the official **audit events table**. Canonical reference: [audit_events.html](https://docs.python.org/3/library/audit_events.html).

---

## Purpose

Audit hooks let **security tools and sandboxes** observe runtime behavior without patching C extensions. Each event name (for example `import`, `compile`, `os.chdir`) maps to a fixed tuple shape described in the upstream table.

---

## How hooks work

| Step | Behavior |
|------|----------|
| Register | `sys.addaudithook(callback)` — callback runs on supported events |
| Event | CPython calls `callback(event, args)` before the operation proceeds |
| Abort | Raising an exception from the hook can block the operation |
| Nesting | Multiple hooks run in registration order |

---

## Example — log import attempts

```python
import sys

events = []

def auditor(event, args):
    if event == "import":
        events.append((event, args[0]))  # module name

sys.addaudithook(auditor)
import json  # noqa: F401 — triggers audit
assert any(name == "json" for _, name in events)
```

---

## Example — block dangerous operations in a sandbox

```python
import sys

def deny_subprocess(event, args):
    if event == "subprocess.Popen":
        raise RuntimeError("subprocess disabled")

sys.addaudithook(deny_subprocess)

try:
    sys.audit("subprocess.Popen", "true", ["true"], {}, -1, -1, -1, -1, False, None, None, None, -1, None, None, None, -1)
except RuntimeError as e:
    assert "subprocess disabled" in str(e)
```

---

## Common event categories

| Category | Example events |
|----------|----------------|
| Import / compile | `import`, `compile`, `exec` |
| Filesystem | `open`, `os.listdir`, `os.mkdir` |
| Network | `socket.connect`, `socket.bind` |
| Process | `subprocess.Popen`, `os.system` |
| Memory | `mmap.mmap`, `ctypes.create_string_buffer` |

See the full table on [audit_events.html](https://docs.python.org/3/library/audit_events.html) for argument tuple layouts.

---

## See also

- [`sys.addaudithook`](https://docs.python.org/3/library/sys.html#sys.addaudithook)
- [PEP 578 — Python Runtime Audit Hooks](https://peps.python.org/pep-0578/)
