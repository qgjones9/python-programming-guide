# [ssl — TLS/SSL wrapper for socket objects](https://docs.python.org/3/library/ssl.html)

The [`ssl`](https://docs.python.org/3/library/ssl.html) module wraps [`socket`](../socket-low-level-networking-interface/index.md) objects with **TLS** using OpenSSL. Prefer **`SSLContext`** + **`wrap_socket()`** over legacy module-level helpers. Read upstream **Security considerations** before deploying. **Optional module** on some builds; **not available on WASI.**

---

## SSLContext — [SSLContext](https://docs.python.org/3/library/ssl.html#sslcontext)

| Method / attribute | Role |
|--------------------|------|
| `create_default_context(purpose)` | Secure defaults for client or server auth |
| `load_cert_chain(certfile, keyfile)` | Server (or mutual TLS) identity |
| `load_verify_locations(cafile=...)` | Trust store for peer verification |
| `wrap_socket(sock, server_side=..., server_hostname=...)` | Returns `SSLSocket` |
| `verify_mode` | `CERT_NONE`, `CERT_OPTIONAL`, `CERT_REQUIRED` |
| `check_hostname` | Enforce name match when verifying |

```python
# Goal: build client and server contexts with safe protocol constants
import ssl

client_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
assert client_ctx.verify_mode == ssl.CERT_REQUIRED
assert ssl.OP_NO_SSLv3 in client_ctx.options
```

```python
# Goal: inspect default cipher list without opening a network connection
import ssl

ctx = ssl.create_default_context()
ciphers = ctx.get_ciphers()
names = {c["name"] for c in ciphers}
assert len(names) > 0
assert all("RC4" not in n for n in names)  # defaults exclude RC4
```

---

## Certificate helpers — [Certificates](https://docs.python.org/3/library/ssl.html#certificates)

| Function | Role |
|----------|------|
| `ssl.get_server_certificate(addr)` | Fetch PEM cert from host (blocking network) |
| `SSLSocket.getpeercert()` | Dict of peer fields after handshake |
| `ssl.DER_cert_to_PEM_cert` / `PEM_cert_to_DER_cert` | Format conversion |

```python
# Goal: map verify_mode integers to documented constants
import ssl

modes = {
    ssl.CERT_NONE: "none",
    ssl.CERT_OPTIONAL: "optional",
    ssl.CERT_REQUIRED: "required",
}
ctx = ssl.create_default_context()
assert modes[ctx.verify_mode] == "required"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Read upstream **Security considerations** | Defaults may be wrong for your threat model |
| Pass **`server_hostname`** on clients | Enables SNI and hostname checks |
| Load explicit **CA bundles** for private PKI | System store may not trust internal CAs |
| Disable SSLv3 only via documented `options` flags | Do not roll custom weak cipher lists casually |
| Use **`ssl.PROTOCOL_TLS_CLIENT` / `SERVER`** | Legacy `PROTOCOL_SSLv23` is deprecated |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| `CERT_NONE` in production | Use `create_default_context()` |
| Certificate hostname mismatch | Set `check_hostname=True` and correct `server_hostname` |
| Mixing blocking socket with handshake | Use timeouts or non-blocking + selector |
| Optional module missing | Catch `ImportError`; document OpenSSL dependency |

---

## See also

- [`socket`](../socket-low-level-networking-interface/index.md) — underlying transport
- [SSL/TLS security considerations](https://docs.python.org/3/library/ssl.html#ssl-security)