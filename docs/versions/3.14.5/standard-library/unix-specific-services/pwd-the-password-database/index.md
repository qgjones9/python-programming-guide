# [pwd — The password database](https://docs.python.org/3/library/pwd.html)

The [`pwd`](https://docs.python.org/3/library/pwd.html) module reads the **Unix user account database** (`/etc/passwd`, NIS, LDAP via nss). It returns **`struct_passwd`** records with login name, UID, GID, home directory, and shell path. Unix-only. Full API remains on [docs.python.org](https://docs.python.org/3/library/pwd.html).

Related: [`grp`](../grp-the-group-database/index.md); [`os.getuid`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md).

---

## Core functions

| Function | Role |
|----------|------|
| `pwd.getpwall()` | Iterator over all entries |
| `pwd.getpwuid(uid)` | Lookup by numeric UID |
| `pwd.getpwnam(name)` | Lookup by login name |

```python
# Goal: lookup current user by UID (Unix)
import importlib.util
import os
import sys

if importlib.util.find_spec("pwd"):
    import pwd

    entry = pwd.getpwuid(os.getuid())
    assert entry.pw_uid == os.getuid()
    assert entry.pw_dir
    assert isinstance(entry.pw_name, str)
else:
    assert sys.platform == "win32"
```

---

## `struct_passwd` fields

| Field | Meaning |
|-------|---------|
| `pw_name` | Login name |
| `pw_passwd` | Password field (often `'x'` → shadow) |
| `pw_uid` / `pw_gid` | Numeric user and primary group ID |
| `pw_gecos` | Full name / GECOS |
| `pw_dir` | Home directory path |
| `pw_shell` | Default login shell |

```python
# Goal: resolve username to home directory (Unix)
import importlib.util
import os

if importlib.util.find_spec("pwd"):
    import pwd

    me = pwd.getpwuid(os.getuid())
    assert os.path.isdir(me.pw_dir)
    by_name = pwd.getpwnam(me.pw_name)
    assert by_name.pw_uid == me.pw_uid
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`Path.home()`** for home dir when sufficient | Works cross-platform |
| Cache **`getpwall()`** sparingly | Can be large on enterprise LDAP |
| Do not trust **`pw_passwd`** for auth | Use `spwd` / PAM / identity providers |

---

## See also

- [`grp`](../grp-the-group-database/index.md) — group database
- [`os.getuid`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) — current UID
