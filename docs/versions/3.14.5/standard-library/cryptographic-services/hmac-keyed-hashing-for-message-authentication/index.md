# [hmac — Keyed-Hashing for Message Authentication](https://docs.python.org/3/library/hmac.html)

The [`hmac`](https://docs.python.org/3/library/hmac.html) module implements **HMAC** (RFC 2104): a secret key combined with a cryptographic hash to authenticate messages. Use it for API signatures, cookie integrity, and webhook verification. Requires a **fixed-length** digest algorithm from [`hashlib`](../hashlib-secure-hashes-and-message-digests/index.md)—**SHAKE** XOF hashes are not supported. Full `HMAC` object details remain on [docs.python.org](https://docs.python.org/3/library/hmac.html).

---

## API — [Module functions](https://docs.python.org/3/library/hmac.html)

| Function / method | Role |
|-------------------|------|
| `hmac.new(key, msg=None, *, digestmod)` | Create HMAC context (`digestmod` required since 3.8) |
| `hmac.digest(key, msg, digest)` | One-shot optimized digest (3.7+) |
| `HMAC.update(msg)` | Feed more message bytes |
| `HMAC.digest()` / `hexdigest()` | Final MAC bytes or hex string |
| `HMAC.copy()` | Clone state for shared-prefix messages |
| `hmac.compare_digest(a, b)` | Constant-time equality for bytes or ASCII str |

`key` must be `bytes` or `bytearray`. `digestmod` is a hash name, constructor, or module accepted by `hashlib.new()`.

```python
# Goal: compute and verify HMAC-SHA256
import hmac
import hashlib

key = b"super-secret-key"
message = b"request-body"
mac = hmac.new(key, message, hashlib.sha256)
expected = mac.hexdigest()
received = hmac.new(key, message, hashlib.sha256).hexdigest()
assert hmac.compare_digest(expected, received)
```

```python
# Goal: incremental update equals concatenation
import hmac
import hashlib

key = b"k"
a, b = b"hello ", b"world"
m1 = hmac.new(key, digestmod=hashlib.sha256)
m1.update(a)
m1.update(b)
m2 = hmac.new(key, a + b, hashlib.sha256)
assert m1.digest() == m2.digest()
```

```python
# Goal: one-shot hmac.digest matches HMAC object
import hmac
import hashlib

key = b"key"
msg = b"msg"
one_shot = hmac.digest(key, msg, "sha256")
obj = hmac.new(key, msg, hashlib.sha256).digest()
assert hmac.compare_digest(one_shot, obj)
```

---

## Verification pattern

Always compare MACs with **`compare_digest`**, not `==`, to reduce timing attack surface.

```python
# Goal: reject tampered message
import hmac
import hashlib

def sign(key, msg):
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

key = b"api-key"
msg = b"data"
tag = sign(key, msg)
bad_msg = b"datb"
assert not hmac.compare_digest(tag, sign(key, bad_msg))
assert hmac.compare_digest(tag, sign(key, msg))
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Pass **`digestmod` as keyword** | Required positional rule since 3.8 |
| Use **SHA-256** or stronger hash | Legacy MD5/SHA-1 HMAC weakens over time |
| Compare with **`compare_digest`** | Avoids content-based short-circuit timing |
| Use **`hmac.digest`** for in-memory one-shots | Faster C path when available |
| Keep **keys long and random** | Short keys brute-force faster |
| Include **timestamp/nonce** in signed payload | Prevents replay at application layer |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| SHAKE as `digestmod` | Not supported | SHA-2/SHA-3 fixed output only |
| `==` on hexdigest strings | Timing leak | `compare_digest` |
| Encoding unicode message ad hoc | Cross-platform MAC mismatch | Encode to bytes explicitly (UTF-8) |
| Reusing `(key, nonce)` pairs in custom schemes | Forgery/replay | Follow standard protocol (TLS, JWT libs) |
| Confusing HMAC with encryption | HMAC does not secrecy | Encrypt separately if needed |
| Missing `digestmod=` keyword | `TypeError` on 3.8+ | Always keyword: `digestmod=hashlib.sha256` |
