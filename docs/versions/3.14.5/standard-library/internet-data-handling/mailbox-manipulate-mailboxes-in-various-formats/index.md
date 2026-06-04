# [mailbox — Manipulate mailboxes in various formats](https://docs.python.org/3/library/mailbox.html)

The [`mailbox`](https://docs.python.org/3/library/mailbox.html) module reads and writes **on-disk mail stores**: **Maildir**, **mbox**, **MH**, **Babyl**, and **MMDF**. It exposes a **mapping-like** API (keys → messages) where iteration yields **message objects**, not keys. Messages extend [`email`](../email-an-email-and-mime-handling-package/index.md). Full format details and locking rules are on [docs.python.org](https://docs.python.org/3/library/mailbox.html).

---

## Supported formats

| Class | Layout | Concurrent access |
|-------|--------|-------------------|
| `mailbox.Maildir` | One file per message in `cur/` / `new/` / `tmp/` | Safest for writers |
| `mailbox.mbox` | Single Unix mbox file | **Lock** required; fragile under parallel write |
| `mailbox.MH` | One file per message, numeric names | Common on Unix MH systems |
| `mailbox.Babyl` | RMAIL Babyl | Legacy |
| `mailbox.MMDF` | Multiple messages with `^A^A^A^A` separators | Legacy |

---

## Maildir workflow

```python
# Goal: create Maildir, add message, read back by key
import mailbox
import os
import tempfile
from email.message import EmailMessage

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "maildir")
    mdir = mailbox.Maildir(path, create=True)
    msg = EmailMessage()
    msg["Subject"] = "Test"
    msg.set_content("Body")
    key = mdir.add(msg)
    assert key in mdir
    fetched = mdir.get_message(key)
    assert fetched["subject"] == "Test"
    mdir.flush()
```

```python
# Goal: iterate messages (values, not keys)
import mailbox
import os
import tempfile
from email.message import EmailMessage

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "maildir")
    mdir = mailbox.Maildir(path, create=True)
    for i in range(3):
        mdir.add(f"Subject: m{i}\n\nmsg {i}\n")
    bodies = [mdir[key].get_payload().strip() for key in sorted(mdir.keys())]
    assert bodies == ["msg 0", "msg 1", "msg 2"]
```

---

## mbox and locking

For `mbox`, call **`lock()`** before changes and **`unlock()`** after. Skipping locks risks corruption if another process touches the file.

```python
# Goal: mbox add/remove with lock around mutation
import mailbox
import tempfile

with tempfile.NamedTemporaryFile(suffix=".mbox", delete=False) as f:
    path = f.name

mbox = mailbox.mbox(path, create=True)
mbox.lock()
try:
    key = mbox.add("From: a@b.com\n\nHello\n")
    assert mbox[key].get_payload() == "Hello\n"
    mbox.remove(key)
    assert len(mbox) == 0
finally:
    mbox.unlock()
    mbox.close()
```

---

## Dictionary-like API highlights

| Method | Behavior |
|--------|----------|
| `add(message)` | Insert; returns new key |
| `__getitem__(key)` / `get_message(key)` | Fetch representation |
| `__setitem__(key, message)` | Replace existing |
| `remove(key)` / `discard(key)` | Delete (`discard` ignores missing) |
| `get_bytes(key)` | Raw bytes (3.2+) |
| `get_file(key)` | Binary file-like (context manager) |

Iteration is safe if the mailbox changes: new messages may not appear; removed messages are skipped.

---

## Message factories

Pass `factory=email.message.EmailMessage` (or a subclass) when constructing the mailbox to get modern message objects instead of format-specific subclasses.

```python
# Goal: Maildir returns EmailMessage instances
import mailbox
import os
import tempfile
from email.message import EmailMessage

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "maildir")
    mdir = mailbox.Maildir(path, create=True, factory=EmailMessage)
    key = mdir.add(EmailMessage())
    assert isinstance(mdir[key], EmailMessage)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **Maildir** for concurrent tools | Avoid whole-file rewrite races |
| Always **`flush()`** / **`close()`** after bulk edits | Ensures kernel buffers hit disk |
| Treat keys as **opaque** to that mailbox instance | Keys are not stable across copies |
| Use **`get_bytes`** for archival pipelines | Avoids re-encoding surprises from `get_string` |

---

## See also

- [`email`](../email-an-email-and-mime-handling-package/index.md) — message representation
- [`smtplib`](../../internet-protocols-and-support/smtplib-smtp-protocol-client/index.md) — network delivery
- [`imaplib`](../../internet-protocols-and-support/imaplib-imap4-protocol-client/index.md) — remote mailbox access
