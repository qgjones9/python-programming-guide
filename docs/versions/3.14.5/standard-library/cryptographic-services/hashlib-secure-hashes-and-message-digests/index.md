# [hashlib — Secure hashes and message digests](https://docs.python.org/3/library/hashlib.html)

The [`hashlib`](https://docs.python.org/3/library/hashlib.html) module exposes a uniform interface to **cryptographic hash algorithms**: SHA-2, SHA-3, BLAKE2, legacy MD5/SHA-1, and **SHAKE** variable-length XOF digests. Construct with named functions (`sha256()`, `blake2b()`, …) or `new(name)`. Feed bytes via `update()`; read `digest()` or `hexdigest()`. For non-cryptographic checksums see [`zlib`](../../data-compression-and-archiving/zlib-compression-compatible-with-gzip/index.md). Full OpenSSL availability and FIPS notes remain on [docs.python.org](https://docs.python.org/3/library/hashlib.html).

---

## Algorithms — [Hash algorithms](https://docs.python.org/3/library/hashlib.html#hash-algorithms)

| Category | Constructors |
|----------|--------------|
| SHA-2 | `sha224`, `sha256`, `sha384`, `sha512` |
| SHA-3 | `sha3_224`, `sha3_256`, `sha3_384`, `sha3_512` |
| SHAKE (XOF) | `shake_128`, `shake_256` — pass **length** to `digest(n)` |
| BLAKE2 | `blake2b`, `blake2s` (optional `key=` for MAC mode) |
| Legacy | `md5`, `sha1` (avoid for new security designs) |

| Attribute | Meaning |
|-----------|---------|
| `algorithms_guaranteed` | Always available in this module |
| `algorithms_available` | Present in running interpreter (may include OpenSSL extras) |

All constructors accept keyword-only **`usedforsecurity=True`** (3.9+); set `False` for non-security hashing when FIPS blocks weak algorithms.

```python
# Goal: incremental SHA-256 matches one-shot
import hashlib

parts = [b"Nobody inspects", b" the spammish repetition"]
expected = hashlib.sha256(b"".join(parts)).hexdigest()

m = hashlib.sha256()
for part in parts:
    m.update(part)
assert m.hexdigest() == expected
```

```python
# Goal: generic new() and copy() for shared prefix
import hashlib

data = b"prefix-suffix"
base = hashlib.new("sha256", b"prefix-")
clone = base.copy()
clone.update(b"suffix")
assert clone.hexdigest() == hashlib.sha256(data).hexdigest()
```

```python
# Goal: SHAKE variable-length output
import hashlib

shake = hashlib.shake_128(b"input")
d16 = shake.digest(16)
d32 = hashlib.shake_128(b"input").digest(32)
assert len(d16) == 16 and len(d32) == 32 and d16 == d32[:16]
```

---

## File hashing — [hashlib.file_digest()](https://docs.python.org/3/library/hashlib.html)

`file_digest(fileobj, digest, /, *, _blocksize=2**20)` (3.11+) returns a hash object after reading a **binary** file object—preferred over manual chunk loops for large files.

```python
# Goal: hash in-memory binary stream with file_digest
import hashlib
import io

payload = b"file contents for hashing"
buf = io.BytesIO(payload)
result = hashlib.file_digest(buf, "sha256")
assert result.hexdigest() == hashlib.sha256(payload).hexdigest()
```

---

## Password-based keys — [Key derivation](https://docs.python.org/3/library/hashlib.html#key-derivation)

`hashlib.scrypt(password, *, salt, n, r, p, maxmem=0, dklen=64)` derives keys for storage protocols (prefer dedicated password libraries for web apps).

```python
# Goal: scrypt derives deterministic key from password + salt
import hashlib

salt = b"unique-salt-bytes"
dk = hashlib.scrypt(b"user-password", salt=salt, n=2**14, r=8, p=1, dklen=32)
assert len(dk) == 32
assert dk == hashlib.scrypt(b"user-password", salt=salt, n=2**14, r=8, p=1, dklen=32)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **SHA-256** or **BLAKE2b** for new fingerprints | MD5/SHA-1 collision weaknesses |
| Prefer **named constructors** over `new("sha256")` | Faster and clearer |
| Use **`file_digest`** for large files | Constant memory streaming |
| Set **`usedforsecurity=False`** for cache keys only | Documents intent; satisfies FIPS builds |
| Compare digests with **`hmac.compare_digest`** | Mitigates timing leaks |
| Do not use bare SHA256 for **password storage** | Use scrypt/argon2/bcrypt with salt |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| MD5/SHA-1 for signatures | Collision attacks | Upgrade to SHA-256+ |
| SHAKE with HMAC | XOF not supported by HMAC | Fixed-length hash only |
| Forgetting `& 0xFFFFFFFF` on CRC-style use | N/A for hashlib but common confusion | hashlib digests are full-width bytes |
| Assuming all OpenSSL algos exist | `ValueError` from `new()` | Check `algorithms_available` |
| `digest()` vs `hexdigest()` mix-ups | Binary vs hex string | Pick one format at API boundaries |
| Reusing salt with scrypt | Rainbow tables | Unique random salt per user |
