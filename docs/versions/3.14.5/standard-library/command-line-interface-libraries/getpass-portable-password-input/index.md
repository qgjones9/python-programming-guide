# [getpass — Portable password input](https://docs.python.org/3/library/getpass.html)

The [`getpass`](https://docs.python.org/3/library/getpass.html) module prompts for **secrets without echoing** to the terminal and resolves a **login name** from the environment. It is the portable choice over ad hoc `input()` for passwords. Full API remains on [docs.python.org](https://docs.python.org/3/library/getpass.html).

**Availability:** not supported on WASI/WebAssembly. Prefer guarding imports in portable CLIs.

---

## Functions

| Function | Role |
|----------|------|
| `getpass(prompt='Password: ', stream=None, *, echo_char=None)` | Read a password; default hides input; 3.14+ `echo_char` masks with a visible character |
| `getuser()` | Return login name from `LOGNAME`, `USER`, `LNAME`, `USERNAME`, or `pwd` |
| `GetPassWarning` | Issued when echo-free input may fall back to visible stdin |

---

## getuser() — [getpass.getuser](https://docs.python.org/3/library/getpass.html#getpass.getuser)

`getuser()` checks environment variables in order and falls back to the password database via [`pwd`](https://docs.python.org/3/library/pwd.html). Prefer it over [`os.getlogin()`](https://docs.python.org/3/library/os.html#os.getlogin) for portability.

```python
# Goal: resolve a non-empty login name on typical Unix/macOS/Linux
import getpass
import os

user = getpass.getuser()
assert isinstance(user, str) and len(user) > 0
# getuser reads env before pwd; setting USER is enough for this check
os.environ.setdefault("USER", user)
assert getpass.getuser() == os.environ["USER"]
```

---

## getpass() behavior

| Topic | Detail |
|-------|--------|
| Echo | Disabled by default; terminal uses `/dev/tty` when available |
| `echo_char='*'` (3.14+) | Shows mask character per keystroke; disables line-editing shortcuts on Unix |
| Fallback | If no TTY, warns and may read from `sys.stdin` (visible) |
| IDLE | Input may appear in the terminal that launched IDLE, not the GUI window |

Interactive `getpass()` cannot run in headless `exec` validation; use mocks in unit tests:

```python
# Goal: simulate getpass in tests with unittest.mock
import getpass
from unittest.mock import patch

with patch("getpass.getpass", return_value="s3cr3t"):
    token = getpass.getpass("Token: ")
assert token == "s3cr3t"
```

---

## CLI integration patterns

| Practice | Why |
|----------|-----|
| Prompt on **`/dev/tty`**, not stdout | Keeps password off piped/logged stdout |
| Combine with **`getuser()`** for “username@host” prompts | Avoid trusting `$USER` alone in setuid contexts |
| Never **`print(password)`** or log the return value | Secrets belong only in memory |
| Offer **`--password-file`** or env vars for automation | Non-interactive CI should not hang on getpass |

```python
# Goal: build a username@host label for a prompt string
import getpass
import socket

label = f"{getpass.getuser()}@{socket.gethostname()}"
assert "@" in label and label.split("@")[0]
```

---

## Related modules

| Module | Relationship |
|--------|--------------|
| [`argparse`](../argparse-parser-for-command-line-options-arguments-and-subcommands/index.md) | Declare `--password` flags; call `getpass()` when flag omitted |
| [`readline`](../../text-processing-services/readline-gnu-readline-interface/index.md) | Not used for hidden input; getpass uses tty layer |
| [`secrets`](https://docs.python.org/3/library/secrets.html) | Generate tokens; getpass collects them from users |
