# [Security Considerations](https://docs.python.org/3/library/security_warnings.html)

Several standard-library modules are **safe only in the right context**. The upstream page [security_warnings.html](https://docs.python.org/3/library/security_warnings.html) links module-specific guidance; this page collects **risk**, **mitigation**, and **repo cross-links** so you can harden scripts and services on Python 3.14.

---

## Module-specific risks

| Module | Risk | Mitigation |
|--------|------|------------|
| [`base64`](../internet-data-handling/base64-base16-base32-base64-base85-data-encodings/index.md) | Not encryption; padding/oracle issues in protocols | Follow [RFC 4648 security considerations](https://www.rfc-editor.org/rfc/rfc4648#section-12); use TLS for secrecy |
| [`hashlib`](../cryptographic-services/hashlib-secure-hashes-and-message-digests/index.md) | Legacy algorithms (MD5, SHA-1) blocked in security contexts | Pass `usedforsecurity=False` only for non-crypto checksums; use SHA-256+ for integrity |
| [`http.server`](../internet-protocols-and-support/httpserver-http-servers/index.md) | Toy server; weak defaults | Use production WSGI/ASGI servers behind TLS termination |
| [`logging`](../generic-operating-system-services/logging-logging-facility-for-python/index.md) | `logging.config` may **`eval`** config strings | Load configs from trusted files only; prefer programmatic setup |
| [`multiprocessing`](../concurrent-execution/multiprocessing-process-based-parallelism/index.md) | `Connection.recv()` unpickles bytes | Only connect trusted peers; never expose listener to the internet |
| [`pickle`](../data-persistence/pickle-python-object-serialization/index.md) | Arbitrary code execution on load | Never unpickle untrusted data; restrict globals per upstream docs |
| [`random`](../numeric-and-mathematical-modules/random-generate-pseudo-random-numbers/index.md) | Predictable PRNG | Use [`secrets`](../cryptographic-services/secrets-generate-secure-random-numbers-for-managing-secrets/index.md) for tokens/passwords |
| [`shelve`](../data-persistence/shelve-python-object-persistence/index.md) | Built on pickle | Treat DB files like pickle blobs—trusted writers only |
| [`ssl`](../networking-and-interprocess-communication/ssl-tlsssl-wrapper-for-socket-objects/index.md) | Certificate validation, protocol versions | Enable hostname check, modern TLS, updated trust store |
| [`subprocess`](../concurrent-execution/subprocess-subprocess-management/index.md) | Shell injection with `shell=True` | Pass argument lists; sanitize paths from users |
| [`tempfile`](../file-and-directory-access/tempfile-generate-temporary-files-and-directories/index.md) | `mktemp()` race | Use `TemporaryDirectory`, `NamedTemporaryFile`, `mkstemp` |
| `xml` ([ElementTree](../structured-markup-processing-tools/xmletreeelementtree-the-elementtree-xml-api/index.md), [Expat](../structured-markup-processing-tools/xmlparsersexpat-fast-xml-parsing-using-expat/index.md), …) | Billion laughs, external entities | `defusedxml` for untrusted XML; disable dangerous features |
| [`zipfile`](../data-compression-and-archiving/zipfile-work-with-zip-archives/index.md) | Zip bombs / disk exhaustion | Limit uncompressed size, member count, and extraction path |

---

## Interpreter startup hardening

| Mechanism | Effect |
|-----------|--------|
| **`-I`** (isolated mode) | Ignores `PYTHON*` env vars, user site, and other convenient but risky paths |
| **`-P`** | Does not prepend unsafe entries to `sys.path` (cwd, script dir, empty string) |
| **`PYTHONSAFEPATH`** | Same path-hardening behavior as `-P` when set |

Use **`-I`** when you cannot trust the environment (shared login nodes, embedded launchers). Combine with **`-P`** when you must run a script but want to avoid importing attacker-controlled modules from the current working directory.

```python
# Goal: demonstrate why secrets beats random for tokens
import random
import secrets

# random is predictable given enough output; secrets uses OS CSPRNG
token = secrets.token_hex(16)
assert len(token) == 32
assert isinstance(secrets.token_urlsafe(8), str)
# random.random() is fine for simulations, not session IDs
assert 0.0 <= random.random() < 1.0
```

```python
# Goal: hashlib blocks insecure algorithms in security-sensitive contexts by default
import hashlib

digest = hashlib.sha256(b"payload", usedforsecurity=True).hexdigest()
assert len(digest) == 64
# usedforsecurity=False allows md5 for non-crypto fingerprints only
legacy = hashlib.md5(b"cache-key", usedforsecurity=False).hexdigest()
assert len(legacy) == 32
```

```python
# Goal: subprocess without shell=True avoids injection on metacharacters
import subprocess

completed = subprocess.run(
    ["printf", "%s", "safe"],
    check=True,
    capture_output=True,
    text=True,
)
assert completed.stdout == "safe"
```

```python
# Goal: tempfile APIs that create private paths (avoid mktemp races)
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "data.txt"
    path.write_text("x", encoding="utf-8")
    assert path.read_text(encoding="utf-8") == "x"
```

```python
# Goal: never unpickle untrusted bytes — use JSON or signed formats instead
import json

payload = {"role": "guest"}
blob = json.dumps(payload).encode("utf-8")
assert json.loads(blob)["role"] == "guest"
```

---

## Pickle and multiprocessing

| API | Rule |
|-----|------|
| `pickle.load` / `loads` | Trusted source only; consider `pickle.Unpickler` with restricted `find_class` |
| `shelve.open` | Same trust model as pickle |
| `multiprocessing.connection.recv` | Peers must be same security domain |

For cross-process data on hostile networks, prefer **JSON**, **msgpack** with schema validation, or **TLS-authenticated** channels—not pickle.

---

## XML and ZIP hardening checklist

| Check | XML | ZIP |
|-------|-----|-----|
| Limit expansion | Cap entity expansion / use defused libraries | Track cumulative uncompressed bytes |
| Reject surprises | Disable external entities | Reject `..` path members (zip slip) |
| Timeouts | Parser timeouts on network input | Stream members instead of extracting all |

---

## Official deep dives

| Topic | Upstream anchor |
|-------|-----------------|
| Pickle restrictions | [pickle — Restricting globals](https://docs.python.org/3/library/pickle.html#restricting-globals) |
| Subprocess safety | [subprocess — Security considerations](https://docs.python.org/3/library/subprocess.html#security-considerations) |
| SSL/TLS | [ssl — SSL/TLS security considerations](https://docs.python.org/3/library/ssl.html#ssl-security-considerations) |
| XML | [xml — XML security](https://docs.python.org/3/library/xml.html#xml-security) |
| zipfile | [zipfile — Decompression pitfalls](https://docs.python.org/3/library/zipfile.html) |

---

## See also

- [Removed Modules](../removed-modules/index.md) — legacy modules dropped from the stdlib
- [Cryptographic Services hub](../cryptographic-services/index.md) — `hashlib`, `secrets`, `hmac`
- [Data Persistence hub](../data-persistence/index.md) — `pickle`, `shelve`, `copyreg`
