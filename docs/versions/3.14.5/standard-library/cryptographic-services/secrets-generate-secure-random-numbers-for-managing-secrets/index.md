# [secrets — Generate secure random numbers for managing secrets](https://docs.python.org/3/library/secrets.html)

The [`secrets`](https://docs.python.org/3/library/secrets.html) module (3.6+) generates **cryptographically strong** random numbers for passwords, tokens, and reset links. It wraps the OS CSPRNG via `SystemRandom`. Use it instead of [`random`](../numeric-and-mathematical-modules/random-generate-pseudo-random-numbers-with-various-distributions/index.md), which is for simulation—not security. Token length guidance and recipes remain on [docs.python.org](https://docs.python.org/3/library/secrets.html).

---

## Random primitives — [Random numbers](https://docs.python.org/3/library/secrets.html#random-numbers)

| Function | Returns |
|----------|---------|
| `secrets.choice(seq)` | Random element from non-empty sequence |
| `secrets.randbelow(n)` | Int in `[0, n)` |
| `secrets.randbits(k)` | Non-negative int with `k` random bits |
| `secrets.SystemRandom` | Class mirroring `random.SystemRandom` |

```python
# Goal: randbelow and randbits stay in range
import secrets

n = secrets.randbelow(100)
assert 0 <= n < 100
bits = secrets.randbits(8)
assert 0 <= bits < 256
```

---

## Token helpers — [Generating tokens](https://docs.python.org/3/library/secrets.html#generating-tokens)

| Function | Output |
|----------|--------|
| `token_bytes(nbytes=None)` | Raw random bytes |
| `token_hex(nbytes=None)` | Hex string (2 chars per byte) |
| `token_urlsafe(nbytes=None)` | URL-safe Base64 text (~1.3 chars/byte) |

When `nbytes` is omitted, **`DEFAULT_ENTROPY`** bytes are used (32 by policy—subject to change).

```python
# Goal: token helpers produce expected shapes
import secrets

raw = secrets.token_bytes(16)
hex_tok = secrets.token_hex(16)
url_tok = secrets.token_urlsafe(16)
assert len(raw) == 16
assert len(hex_tok) == 32
assert all(c.isalnum() or c in "-_" for c in url_tok)
```

```python
# Goal: build an alphanumeric password with secrets.choice
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(12))
assert len(password) == 12
assert all(c in alphabet for c in password)
```

---

## Constant-time compare — [compare_digest](https://docs.python.org/3/library/secrets.html#secrets.compare_digest)

`secrets.compare_digest(a, b)` delegates to the same constant-time logic as [`hmac.compare_digest`](../hmac-keyed-hashing-for-message-authentication/index.md).

```python
# Goal: compare_digest for token verification
import secrets

token = secrets.token_hex(32)
assert secrets.compare_digest(token, token)
assert not secrets.compare_digest(token, secrets.token_hex(32))
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **≥32 bytes** (`DEFAULT_ENTROPY`) for session tokens | 256-bit brute-force margin |
| Prefer **`token_urlsafe`** in URLs | No quoting issues vs hex |
| Never store passwords **recoverable** | Hash with scrypt/argon2/bcrypt + salt |
| Use **`compare_digest`** when checking tokens | Timing-safe equality |
| Do not seed or instantiate **`random`** for secrets | MT is deterministic given state |
| Regenerate token on **every** password reset | Old links must invalidate |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `random.choice` for passwords | Predictable tokens | `secrets.choice` |
| Short 4-digit PIN as only secret | Trivial brute force | Long `token_urlsafe` or MFA |
| Storing token in URL logs | Leak via Referer/logs | POST body or HttpOnly cookie |
| Assuming `DEFAULT_ENTROPY` is fixed | May change in maintenance releases | Pass explicit `nbytes` if you must |
| `compare_digest` on different types | Always false / error path | Both str or both bytes-like |
| XKCD passphrase without enough words | Reduced entropy | Use 4+ words from large dict |
