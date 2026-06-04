# [netrc — netrc file processing](https://docs.python.org/3/library/netrc.html)

The [`netrc`](https://docs.python.org/3/library/netrc.html) module parses **`.netrc`** files used by FTP clients and similar tools to store **host login credentials**. A `netrc` instance maps host names to `(login, account, password)` tuples and supports **macro** definitions. On POSIX, insecure file permissions trigger `NetrcParseError`. Full security checks and parsing rules remain on [docs.python.org](https://docs.python.org/3/library/netrc.html).

---

## API — [netrc Objects](https://docs.python.org/3/library/netrc.html#netrc-objects)

| Symbol | Role |
|--------|------|
| `netrc([file])` | Parse file path or default `~/.netrc` |
| `authenticators(host)` | Return `(login, account, password)` or `None` |
| `.hosts` | `dict` mapping host → credential tuple |
| `.macros` | `dict` mapping macro name → token list |
| `NetrcParseError` | Syntax errors with `msg`, `filename`, `lineno` |

If no entry matches `host`, **`default`** is used when present.

```python
# Goal: parse a netrc file and look up credentials
import netrc
import tempfile
from pathlib import Path

content = """
machine example.com
login alice
password s3cr3t

default
login anonymous
password guest@example.com
"""
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / ".netrc"
    path.write_text(content, encoding="utf-8")
    n = netrc.netrc(path)
    auth = n.authenticators("example.com")
    assert auth == ("alice", "", "s3cr3t")
    fallback = n.authenticators("unknown.host")
    assert fallback == ("anonymous", "", "guest@example.com")
```

```python
# Goal: round-trip via __repr__
import netrc
import tempfile
from pathlib import Path

original = "machine ftp.test\nlogin bob\npassword pass\n"
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / ".netrc"
    path.write_text(original, encoding="utf-8")
    n = netrc.netrc(path)
    dumped = repr(n)
    roundtrip = Path(tmp) / "roundtrip.netrc"
    roundtrip.write_text(dumped, encoding="utf-8")
    n2 = netrc.netrc(roundtrip)
    assert n2.authenticators("ftp.test") == ("bob", "", "pass")
```

---

## Macros and defaults

| Token | Meaning |
|-------|---------|
| `machine host` | Start entry for named host |
| `default` | Fallback when host not listed |
| `login` / `password` / `account` | Credential fields (account often empty) |
| `macdef name` | Begin macro; lines until blank line |

Missing tokens default to empty strings (3.10+). Login **`anonymous`** skips POSIX permission checks.

---

## Best practices

| Practice | Why |
|----------|-----|
| Restrict **file mode** to user-read/write only (`0600`) | POSIX builds enforce secure permissions |
| Never log **password** fields | netrc stores plaintext secrets |
| Prefer **SSH keys or vault** for new systems | netrc is legacy FTP-oriented |
| Use **`authenticators`** rather than `.hosts` directly | Honors `default` fallback rules |
| Handle **`None`** when host and default missing | Caller must prompt or fail |
| UTF-8 content | Parser tries UTF-8 before locale encoding (3.10+) |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| World-readable `~/.netrc` | `NetrcParseError` on POSIX | `chmod 600 ~/.netrc` |
| Assuming account is always set | Often empty string | Unpack all three tuple elements |
| Storing netrc in version control | Credential leak | `.gitignore` and secret scanning |
| Missing `default` for unknown hosts | `authenticators` returns `None` | Provide explicit fallback logic |
| Parsing untrusted netrc bytes | Plaintext exposure | Treat like any secret file |
| Relying on netrc for non-FTP protocols | Format is FTP-centric | Use proper OAuth/token stores |
