# [smtplib — SMTP protocol client](https://docs.python.org/3/library/smtplib.html)

[`smtplib`](https://docs.python.org/3/library/smtplib.html) sends email via **SMTP**: connect, EHLO/HELO, optional STARTTLS, authenticate, `mail`, `rcpt`, `data`, and quit. Classes: `SMTP`, `SMTP_SSL`, `LMTP`. Reference: [smtplib](https://docs.python.org/3/library/smtplib.html).

---

## Sending workflow

| Step | Method |
|------|--------|
| Connect | `SMTP(host, port=25, timeout=...)` |
| Greet | `ehlo()` or `helo()` |
| TLS | `starttls(context=...)` when server advertises STARTTLS |
| Auth | `login(user, password)` if required |
| Envelope | `mail(from_addr)`, `rcpt(to_addrs)` |
| Body | `data(message_bytes)` — must use CRLF lines ending with `\r\n.\r\n` |

Higher-level helpers: `sendmail`, `send_message` (with [`email`](../../internet-data-handling/email-an-email-and-mime-handling-package/index.md) package).

---

## Example — address quoting helper

```python
# Goal: format RFC 5322 addresses for SMTP commands
import smtplib

assert smtplib.quoteaddr("ada@example.com") == "<ada@example.com>"
assert smtplib.SMTP.default_port == 25
assert issubclass(smtplib.SMTPException, Exception)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`SMTP_SSL`** or **`starttls`** | Plain SMTP leaks credentials and content |
| Set **timeouts** | Prevent hung MTA connections |
| Prefer **`send_message`** | Handles encoding and headers vs raw `data` |

---

## Debugging

`smtplib` module-level `debuglevel` prints protocol chatter to stderr—useful in development only.
