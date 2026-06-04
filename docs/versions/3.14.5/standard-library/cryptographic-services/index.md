# [Cryptographic Services](https://docs.python.org/3/library/crypto.html)

The standard library provides **hash functions**, **message authentication**, and **cryptographically secure randomness** for application security. Use [`hashlib`](hashlib-secure-hashes-and-message-digests/index.md) for SHA-2/SHA-3/BLAKE2 digests; [`hmac`](hmac-keyed-hashing-for-message-authentication/index.md) for keyed MACs over those hashes; [`secrets`](secrets-generate-secure-random-numbers-for-managing-secrets/index.md) for tokens and passwords (never use [`random`](../numeric-and-mathematical-modules/random-generate-pseudo-random-numbers/index.md) for secrets). Algorithm availability depends on the build (OpenSSL, FIPS mode). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/crypto.html).

Related material: [`ssl`](../networking-and-interprocess-communication/ssl-tlsssl-wrapper-for-socket-objects/index.md) for TLS, [`hashlib.file_digest`](hashlib-secure-hashes-and-message-digests/index.md) for streaming file hashes, and [`base64`](../internet-data-handling/base64-base16-base32-base64-base85-data-encodings/index.md) for encoding digests.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`hashlib`](hashlib-secure-hashes-and-message-digests/index.md) | SHA-2, SHA-3, BLAKE2, MD5, SHAKE variable-length digests |
| [`hmac`](hmac-keyed-hashing-for-message-authentication/index.md) | RFC 2104 HMAC; constant-time `compare_digest` |
| [`secrets`](secrets-generate-secure-random-numbers-for-managing-secrets/index.md) | Secure tokens, `choice`, `compare_digest` for secrets |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Fingerprint a file or message | [`hashlib.sha256`](hashlib-secure-hashes-and-message-digests/index.md) (or SHA-3/BLAKE2) |
| Verify API/webhook signatures | [`hmac.new`](hmac-keyed-hashing-for-message-authentication/index.md) + `compare_digest` |
| Password reset / session token URL | [`secrets.token_urlsafe`](secrets-generate-secure-random-numbers-for-managing-secrets/index.md) |
| Compare hex digests safely | `hmac.compare_digest` or `secrets.compare_digest` |
| Non-security checksum (cache key) | `hashlib` with `usedforsecurity=False` when appropriate |
| Password **storage** | Dedicated KDF (e.g. `hashlib.scrypt`, `bcrypt` on PyPI)—not plain SHA256 |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Use **`secrets`**, not **`random`**, for credentials | Mersenne Twister is predictable |
| Compare digests with **`compare_digest`** | Plain `==` leaks timing information |
| Prefer **SHA-256+** for new designs | MD5/SHA-1 have known collision attacks |
| Pass **`usedforsecurity=False`** only for non-crypto hashes | FIPS builds may block weak algorithms otherwise |
| Use **≥32 bytes** (`DEFAULT_ENTROPY`) for tokens | Resists brute-force as hardware improves |
| Never roll your own **MAC or encryption** | Compose stdlib primitives or vetted libraries |

```python
# Goal: SHA-256 digest of a message
import hashlib

msg = b"Nobody inspects the spammish repetition"
digest = hashlib.sha256(msg).hexdigest()
assert len(digest) == 64
assert hashlib.sha256(msg).digest() == bytes.fromhex(digest)
```

```python
# Goal: HMAC-SHA256 and constant-time verify
import hmac
import hashlib

key = b"shared-secret"
msg = b"payload"
mac = hmac.new(key, msg, hashlib.sha256).hexdigest()
assert hmac.compare_digest(mac, hmac.new(key, msg, hashlib.sha256).hexdigest())
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `random.randint` for tokens | Predictable values | `secrets.token_hex` / `token_urlsafe` |
| SHA256 alone for password storage | Fast offline cracking | Use scrypt/argon2/bcrypt |
| `==` on MAC or digest strings | Timing side channels | `compare_digest` |
| SHAKE with **HMAC** | Variable-length XOF incompatible with HMAC | Fixed-length SHA-2/SHA-3 only |
| Assuming MD5 always available | Blocked in FIPS Python builds | Check `algorithms_guaranteed` |
| Reusing **nonce/token** | Replay attacks | Generate fresh `secrets` per use |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [hashlib — Secure hashes and message digests](hashlib-secure-hashes-and-message-digests/index.md) | Constructors, `algorithms_*`, SHAKE, `file_digest`, scrypt |
| [hmac — Keyed-Hashing for Message Authentication](hmac-keyed-hashing-for-message-authentication/index.md) | `HMAC` objects, `digest`, `compare_digest` |
| [secrets — Generate secure random numbers for managing secrets](secrets-generate-secure-random-numbers-for-managing-secrets/index.md) | `token_*`, `choice`, `DEFAULT_ENTROPY` |
