# [Removed Modules](https://docs.python.org/3/library/removed.html)

These modules **no longer ship** with CPython (mostly via [PEP 594](https://peps.python.org/pep-0594/) and follow-on cleanups). They remain documented on [docs.python.org](https://docs.python.org/3/library/removed.html) so you can find **removal version**, **historical purpose**, and **migration paths**. Do not `import` them on Python 3.12+ / 3.13+ where noted—use the replacements below or a maintained PyPI package.

---

## Removal timeline (summary)

| Removed in | Examples |
|------------|----------|
| **3.12** | `asyncore`, `asynchat`, `distutils`, `imp`, `smtpd` |
| **3.13** | `aifc`, `audioop`, `cgi`, `crypt`, `telnetlib`, `uu`, `xdrlib`, and most other PEP 594 “dead battery” modules |

Pinned docs for each module: `https://docs.python.org/3/library/<name>.html` (stub pages redirect to removal notes).

---

## Replacement guide

| Module | Removed | Primary migration |
|--------|---------|-------------------|
| `aifc` | 3.13 | [`wave`](../multimedia-services/wave-read-and-write-wav-files/index.md) for WAV; PyPI **`soundfile`** / **`audioread`** for AIFF/AIFC |
| `asynchat` | 3.12 | [`asyncio`](../networking-and-interprocess-communication/asyncio-asynchronous-io/index.md) streams and protocols |
| `asyncore` | 3.12 | [`asyncio`](../networking-and-interprocess-communication/asyncio-asynchronous-io/index.md) event loop |
| `audioop` | 3.13 | NumPy/audio libraries; no direct stdlib successor |
| `cgi` | 3.13 | WSGI/ASGI frameworks (`starlette`, `django`, …); `urllib.parse` + `html.escape` for minimal forms |
| `cgitb` | 3.13 | [`logging`](../generic-operating-system-services/logging-logging-facility-for-python/index.md), `traceback` module, framework debug pages |
| `chunk` | 3.13 | `struct.unpack` / manual fourCC parsing for IFF-style containers |
| `crypt` | 3.13 | **`bcrypt`**, **`argon2-cffi`**, or **`passlib`** — never recreate DES-based `crypt(3)` |
| `distutils` | 3.12 | **`setuptools`**, **`packaging`**; build backends per [PEP 517](https://peps.python.org/pep-0517/) |
| `imghdr` | 3.13 | `mimetypes`, file magic via **`python-magic`**, or Pillow `Image.open` |
| `imp` | 3.12 | [`importlib`](../importing-modules/importlib-the-implementation-of-import/index.md) (`importlib.util`, loaders, `invalidate_caches`) |
| `mailcap` | 3.13 | Application-specific MIME maps; no stdlib replacement |
| `msilib` | 3.13 | Windows installer tooling outside stdlib |
| `nis` | 3.13 | LDAP or platform-specific directory services |
| `nntplib` | 3.13 | PyPI **`nntplib`** fork or HTTP-based APIs |
| `ossaudiodev` | 3.13 | OS audio APIs / PyAudio / sounddevice |
| `pipes` | 3.13 | [`subprocess`](../concurrent-execution/subprocess-subprocess-management/index.md) with explicit argument lists |
| `smtpd` | 3.12 | PyPI **`aiosmtpd`** or dedicated MTA software |
| `sndhdr` | 3.13 | Same as `imghdr` / `wave` / sniffing libraries |
| `spwd` | 3.13 | `pwd` for passwd DB; shadow databases are platform-specific |
| `sunau` | 3.13 | [`wave`](../multimedia-services/wave-read-and-write-wav-files/index.md) for `.wav`; other formats via PyPI |
| `telnetlib` | 3.13 | PyPI **`telnetlib3`** or SSH (`paramiko`, `asyncssh`) |
| `uu` | 3.13 | [`base64`](../internet-data-handling/base64-base16-base32-base64-base85-data-encodings/index.md) or `codecs.encode(..., "uu")` via codecs registry |
| `xdrlib` | 3.13 | [`struct`](../binary-data-services/struct-interpret-bytes-as-packed-binary-data/index.md) with explicit endianness |

---

## Patterns by problem domain

| Domain | Removed pieces | Modern approach |
|--------|----------------|-----------------|
| **CLI / packaging** | `distutils` | `pip install`, `pyproject.toml`, `setuptools` or `hatchling` |
| **Import machinery** | `imp` | `importlib.util.spec_from_file_location`, `importlib.machinery` |
| **Async networking** | `asyncore`, `asynchat` | `asyncio` protocols, `asyncio.start_server` |
| **Shell pipelines** | `pipes` | `subprocess.run([...], check=True)` — avoid `shell=True` with untrusted input |
| **CGI on the web** | `cgi`, `cgitb` | Deploy behind a real app server; never expose raw CGI in production |
| **Audio containers** | `aifc`, `sunau`, `sndhdr`, `audioop` | `wave` + dedicated audio libraries |
| **Encoding wire data** | `uu`, `xdrlib` | `base64` / `struct` |

---

## `imp` → `importlib` (exec example)

```python
# Goal: load a module from a path without imp.load_source (removed in 3.12)
import importlib.util
from pathlib import Path

path = Path("/tmp/demo_module.py")
path.write_text("VALUE = 42\n", encoding="utf-8")
spec = importlib.util.spec_from_file_location("demo_module", path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
assert module.VALUE == 42
path.unlink(missing_ok=True)
```

---

## `uu` → `base64` (exec example)

```python
# Goal: uuencode-style transport using base64 (uu module removed in 3.13)
import base64

raw = b"hello"
encoded = base64.b64encode(raw)
assert base64.b64decode(encoded) == raw
```

---

## `pipes` → `subprocess` (exec example)

```python
# Goal: run a filter pipeline without the pipes module (removed in 3.13)
import subprocess

result = subprocess.run(
    ["python3", "-c", "print('ok')"],
    check=True,
    capture_output=True,
    text=True,
)
assert result.stdout.strip() == "ok"
```

---

## `asyncore` mindset → `asyncio` (exec example)

```python
# Goal: minimal TCP echo server pattern with asyncio (replaces asyncore/asynchat)
import asyncio

async def echo(reader, writer):
    data = await reader.read(100)
    writer.write(data)
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(echo, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    writer.write(b"ping")
    await writer.drain()
    assert await reader.read(4) == b"ping"
    writer.close()
    await writer.wait_closed()
    server.close()
    await server.wait_closed()

asyncio.run(main())
```

---

## See also

- [Superseded Modules](../superseded-modules/index.md) — still importable but discouraged
- [Security Considerations](../security-considerations/index.md) — modules that need extra care when used
- [PEP 594 – Removing dead batteries from the standard library](https://peps.python.org/pep-0594/)
