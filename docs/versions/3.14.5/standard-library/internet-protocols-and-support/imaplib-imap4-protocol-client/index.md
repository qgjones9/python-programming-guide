# [imaplib — IMAP4 protocol client](https://docs.python.org/3/library/imaplib.html)

[`imaplib`](https://docs.python.org/3/library/imaplib.html) implements **IMAP4rev1** client commands: connect, authenticate, `select` a mailbox, `search`, `fetch` messages, `store` flags, and `logout`. Use **`IMAP4_SSL`** for implicit TLS. Reference: [imaplib](https://docs.python.org/3/library/imaplib.html).

---

## Common methods

| Method | Role |
|--------|------|
| `login(user, password)` | Authenticate (consider app passwords/OAuth externally) |
| `select(mailbox='INBOX')` | Open mailbox; returns message count |
| `search(None, 'ALL')` | Return space-separated message ids |
| `fetch(msg_id, '(RFC822)')` | Retrieve full message |
| `store(msg_id, '+FLAGS', '\\Seen')` | Update flags |
| `close()`, `logout()` | Release mailbox and disconnect |

---

## Example — parse IMAP literal size helper

```python
# Goal: exercise imaplib utilities without a live mail server
import imaplib

assert imaplib.IMAP4_PORT == 143
assert imaplib.IMAP4_SSL_PORT == 993
assert issubclass(imaplib.IMAP4.error, Exception)

# Internal: map response codes to readable labels
assert imaplib.Debug >= 0
```

---

## Threading and IDLE

IMAP connections are **stateful**; one connection per thread is typical. Extended commands (`IDLE`, `UID`) follow RFC conventions documented on [docs.python.org](https://docs.python.org/3/library/imaplib.html).

---

## Security

Never log raw credentials. Use TLS (`IMAP4_SSL` or `STARTTLS`) and modern authentication flows required by your provider.
