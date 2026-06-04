# [email — An email and MIME handling package](https://docs.python.org/3/library/email.html)

The [`email`](https://docs.python.org/3/library/email.html) package models, parses, and serializes **RFC 5322** messages and **MIME** bodies. It does **not** send mail — use [`smtplib`](../../internet-protocols-and-support/smtplib-smtp-protocol-client/index.md) for SMTP. The modern stack centers on **`EmailMessage`**, **`policy`**, parsers, and generators; legacy **`compat32`** APIs remain for older code. Full tree of submodules is on [docs.python.org](https://docs.python.org/3/library/email.html).

---

## Architecture

| Component | Role |
|-----------|------|
| `email.message.EmailMessage` | Tree of headers and payloads (unicode-friendly) |
| `email.parser` | Bytes or text stream → `EmailMessage` |
| `email.generator` | `EmailMessage` → serialized bytes |
| `email.policy` | Controls folding, MIME boundaries, SMTP vs HTTP quirks |
| `email.contentmanager` | Set/get typed body content (`set_content`, attachments) |

---

## Building a simple message

```python
# Goal: create plain-text message with Subject and body
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "sender@example.com"
msg["To"] = "recipient@example.com"
msg["Subject"] = "Greetings"
msg.set_content("Hello, world.")
serialized = msg.as_bytes()
assert b"Subject: Greetings" in serialized
assert b"Hello, world." in serialized
```

```python
# Goal: attach binary part with filename and MIME type
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("See attached.")
msg.add_attachment(
    b"\x89PNG\r\n",
    maintype="image",
    subtype="png",
    filename="dot.png",
)
parts = list(msg.iter_attachments())
assert len(parts) == 1 and parts[0].get_filename() == "dot.png"
```

---

## Parsing bytes from disk or wire

```python
# Goal: parse bytes and read headers without manual line splitting
from email import message_from_bytes
from email.policy import default

raw = (
    b"From: parser@example.com\r\n"
    b"To: you@example.com\r\n"
    b"Subject: Parsed\r\n"
    b"\r\n"
    b"Body text.\r\n"
)
msg = message_from_bytes(raw, policy=default)
assert msg["from"] == "parser@example.com"
assert msg.get_content().strip() == "Body text."
```

```python
# Goal: BytesParser for file-like input
from email.parser import BytesParser
from email.policy import default
from io import BytesIO

stream = BytesIO(
    b"Subject: Streamed\r\n\r\nPayload here.\r\n"
)
msg = BytesParser(policy=default).parse(stream)
assert msg["subject"] == "Streamed"
```

---

## Policy and serialization

`policy` objects control maximum line length, whether to use SMTP line endings, and how non-ASCII headers are encoded (RFC 2047). Attach a policy when constructing or parsing; override on `Generator` when emitting for a specific transport.

```python
# Goal: clone message under default policy and re-serialize
from email import policy
from email.message import EmailMessage

msg = EmailMessage(policy=policy.default)
msg["Subject"] = "Café"
msg.set_content("Unicode body: café")
out = msg.as_string()
assert "caf" in out.lower() or "Caf" in out
```

---

## Utilities and iterators

| Submodule | Use |
|-----------|-----|
| `email.utils` | `parseaddr`, `formataddr`, `parsedate_to_datetime` |
| `email.headerregistry` | Typed headers (`Address`, `Date`) |
| `email.iterators` | Walk multiparts (`typed_subpart_iterator`) |

```python
# Goal: parse address tuple for display name and addr
from email.utils import formataddr, parseaddr

display, addr = parseaddr("Alice <alice@example.com>")
assert display == "Alice" and addr == "alice@example.com"
formatted = formataddr(("Bob", "bob@example.com"))
assert "bob@example.com" in formatted
```

---

## Legacy vs modern

| API | When |
|-----|------|
| `EmailMessage` + `policy.default` | **New code** — 3.6+ |
| `email.mime.*` + `MIMEText` | Older tutorials; still works |
| `compat32` `Message` | Maintenance only — exposes RFC details |

---

## Best practices

| Practice | Why |
|----------|-----|
| Parse **bytes** with `BytesParser` | Avoids ambiguous decoding of 8-bit messages |
| Use **`set_content` / `add_attachment`** | Correct MIME boundaries and CTE selection |
| Do not confuse **`email`** with transport | `smtplib.send_message` sends; `email` only formats |
| Validate **attachment size** before parsing | Large MIME trees consume memory |

---

## See also

- [`mailbox`](../mailbox-manipulate-mailboxes-in-various-formats/index.md) — on-disk collections of messages
- [`quopri`](../quopri-encode-and-decode-mime-quoted-printable-data/index.md) — low-level quoted-printable
- [email.parser](https://docs.python.org/3/library/email.parser.html) — `FeedParser`, defects
- [email.contentmanager](https://docs.python.org/3/library/email.contentmanager.html) — typed payloads
