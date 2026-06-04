# [grp — The group database](https://docs.python.org/3/library/grp.html)

The [`grp`](https://docs.python.org/3/library/grp.html) module reads the **Unix group database** (`/etc/group` and nss backends). It returns **`struct_group`** records: group name, GID, member list. Unix-only. Full API remains on [docs.python.org](https://docs.python.org/3/library/grp.html).

Related: [`pwd`](../pwd-the-password-database/index.md); [`os.getgid`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md).

---

## Core functions

| Function | Role |
|----------|------|
| `grp.getgrall()` | Iterator over all groups |
| `grp.getgrgid(gid)` | Lookup by numeric GID |
| `grp.getgrnam(name)` | Lookup by group name |

```python
# Goal: lookup primary group (Unix)
import importlib.util
import os
import sys

if importlib.util.find_spec("grp"):
    import grp

    g = grp.getgrgid(os.getgid())
    assert g.gr_gid == os.getgid()
    assert isinstance(g.gr_name, str)
else:
    assert sys.platform == "win32"
```

---

## `struct_group` fields

| Field | Meaning |
|-------|---------|
| `gr_name` | Group name |
| `gr_passwd` | Password field (often unused) |
| `gr_gid` | Numeric group ID |
| `gr_mem` | List of member usernames |

```python
# Goal: walk groups containing current user (Unix)
import importlib.util
import os

if importlib.util.find_spec("grp"):
    import pwd
    import grp

    user = pwd.getpwuid(os.getuid()).pw_name
    memberships = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
    assert isinstance(memberships, list)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`os.getgid()`** when only primary group matters | Faster than scanning `getgrall` |
| Guard imports on **Windows** | Module not available |
| Prefer **`subprocess` group management tools** for admin tasks | `grp` is read-only |

---

## See also

- [`pwd`](../pwd-the-password-database/index.md) — user database
- [`resource`](../resource-resource-usage-information/index.md) — per-process limits
