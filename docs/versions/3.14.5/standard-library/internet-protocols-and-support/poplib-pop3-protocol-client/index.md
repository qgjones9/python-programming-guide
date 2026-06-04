# [poplib — POP3 protocol client](https://docs.python.org/3/library/poplib.html)

[`poplib`](https://docs.python.org/3/library/poplib.html) speaks **POP3** for retrieving mail from a mailbox: `USER`/`PASS`, `STAT`, `LIST`, `RETR`, `DELE`, optional **`STLS`/`APOP`**, and **`POP3_SSL`**. Reference: [poplib](https://docs.python.org/3/library/poplib.html).

---

## POP3 object workflow

| Phase | Methods |
|-------|---------|
| Connect | `POP3(host)` or `POP3_SSL(host)` |
| Auth | `user(name)`, `pass_(password)` or `apop` |
| Inspect | `stat()`, `list()`, `uidl()` |
| Download | `retr(which)` → `(response, ['line', ...], octets)` |
| Cleanup | `dele(which)`, `quit()` |

---

## Example — module helpers and exceptions

```python
# Goal: verify POP3 line decoding and error types without network
import poplib

assert poplib._MAXLINE > 0
assert poplib.POP3_PORT == 110

assert issubclass(poplib.error_proto, Exception)
assert poplib.POP3_SSL.__name__ == "POP3_SSL"
```

---

## Security

POP3 passwords and message contents are **cleartext** on the wire unless upgraded with STLS or POP3_SSL. Prefer IMAP with TLS for modern mail access when the server supports it.

---

## See also

- [`imaplib`](../imaplib-imap4-protocol-client/index.md) for folder-based mail access
- [`smtplib`](../smtplib-smtp-protocol-client/index.md) for sending mail
