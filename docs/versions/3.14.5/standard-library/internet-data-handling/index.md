# [Internet Data Handling](https://docs.python.org/3/library/netdata.html)

Python’s standard library groups **wire-format and MIME data** under **Internet Data Handling**: JSON for APIs, email/MIME for messages, mailbox formats on disk, and ASCII encodings (base64, quoted-printable, hex). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/netdata.html); this hub orients you to each module and when to reach for it.

Related material outside this section: [`smtplib`](../internet-protocols-and-support/smtplib-smtp-protocol-client/index.md) and [`poplib`](../internet-protocols-and-support/poplib-pop3-protocol-client/index.md) for transport, [`urllib`](../internet-protocols-and-support/urllib-url-handling-modules/index.md) for HTTP, and [`codecs`](../binary-data-services/codecs-codec-registry-and-base-classes/python-specific-encodings/binary-transforms/index.md) for registry-based base64/hex/quopri transforms.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`email`](email-an-email-and-mime-handling-package/index.md) | Parse, build, and serialize RFC 5322 / MIME messages (`EmailMessage`) |
| [`json`](json-json-encoder-and-decoder/index.md) | JSON encode/decode for APIs and config files |
| [`mailbox`](mailbox-manipulate-mailboxes-in-various-formats/index.md) | Read/write Maildir, mbox, MH, Babyl, MMDF on disk |
| [`mimetypes`](mimetypes-map-filenames-to-mime-types/index.md) | Guess `type/subtype` from filenames and extensions |
| [`base64`](base64-base16-base32-base64-base85-data-encodings/index.md) | RFC 4648 and Base85 encodings without MIME line wrapping |
| [`binascii`](binascii-convert-between-binary-and-ascii/index.md) | Low-level hex, CRC, uuencode, base64, quoted-printable |
| [`quopri`](quopri-encode-and-decode-mime-quoted-printable-data/index.md) | Quoted-printable bodies and Q-encoded headers |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| REST/CLI JSON payloads | [`json`](json-json-encoder-and-decoder/index.md) — `loads` / `dumps` / `load` / `dump` |
| Build or parse an email with attachments | [`email`](email-an-email-and-mime-handling-package/index.md) — `EmailMessage`, `policy` |
| Scan a user’s Maildir or mbox archive | [`mailbox`](mailbox-manipulate-mailboxes-in-various-formats/index.md) |
| Set `Content-Type` from `report.pdf` | [`mimetypes`](mimetypes-map-filenames-to-mime-types/index.md) |
| URL-safe tokens in paths or JWT segments | [`base64`](base64-base16-base32-base64-base85-data-encodings/index.md) — `urlsafe_b64encode` |
| Fast hex with optional separators | [`binascii`](binascii-convert-between-binary-and-ascii/index.md) or `bytes.hex()` |
| Mostly-printable MIME body | [`quopri`](quopri-encode-and-decode-mime-quoted-printable-data/index.md) or `email` content manager |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Cap **JSON** size and depth from untrusted sources | Malicious payloads can exhaust CPU/memory |
| Use **`EmailMessage` + `policy`** (3.6+) | Unicode-friendly; avoids legacy `compat32` pitfalls |
| Prefer **`Maildir`** for concurrent mailbox access | Single-file `mbox` corrupts easily under parallel writers |
| Use **`strict=True`** in `mimetypes` for standards-only types | `strict=False` adds common but non-IANA guesses |
| Pick **`base64`** over `codecs` when you need no trailing newline | `base64_codec` always appends `\n` per MIME |
| Validate **decoded binary size** after base64/zlib | Prevents decompression bombs in pipelines |

```python
# Goal: round-trip a small API-shaped dict as JSON bytes
import json

payload = {"status": "ok", "count": 2}
wire = json.dumps(payload, separators=(",", ":")).encode("ascii")
assert json.loads(wire) == payload
```

```python
# Goal: build a minimal MIME message and read a header back
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Hello"
msg.set_content("Plain body")
assert msg["subject"] == "Hello"
assert msg.get_content().strip() == "Plain body"
```

```python
# Goal: filename → Content-Type for an HTTP response
import mimetypes

mime, encoding = mimetypes.guess_type("archive.tar.gz")
assert mime == "application/x-tar" and encoding == "gzip"
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Parsing huge JSON with `json.loads` | Memory/CPU spike | Stream with `JSONDecoder.raw_decode` or limit input size |
| Editing `mbox` without `lock()` | Corrupted mailbox | `lock()` / `unlock()` or switch to Maildir |
| Assuming `guess_type` returns encoding for transfer | Returns compression (gzip), not CTE | Set `Content-Transfer-Encoding` separately |
| Using legacy `email.message.Message` for new code | Bytes/unicode edge cases | `EmailMessage` and `email.policy.default` |
| Confusing **`binascii.b2a_base64`** newline with **`base64.b64encode`** | Extra `\n` in output | Choose module to match consumer (MIME vs RFC 4648) |

---

## Sections in this repo

| Module | Notes |
|--------|-------|
| [email — An email and MIME handling package](email-an-email-and-mime-handling-package/index.md) | `EmailMessage`, parser, generator, policy |
| [json — JSON encoder and decoder](json-json-encoder-and-decoder/index.md) | `dumps`/`loads`, `JSONEncoder`, CLI |
| [mailbox — Manipulate mailboxes in various formats](mailbox-manipulate-mailboxes-in-various-formats/index.md) | Maildir, mbox, locking, iteration |
| [mimetypes — Map filenames to MIME types](mimetypes-map-filenames-to-mime-types/index.md) | `guess_type`, `MimeTypes`, `mime.types` |
| [base64 — Base16, Base32, Base64, Base85 Data Encodings](base64-base16-base32-base64-base85-data-encodings/index.md) | RFC 4648, url-safe, Ascii85/Z85 |
| [binascii — Convert between binary and ASCII](binascii-convert-between-binary-and-ascii/index.md) | Hex, CRC32, strict base64 |
| [quopri — Encode and decode MIME quoted-printable data](quopri-encode-and-decode-mime-quoted-printable-data/index.md) | Bodies vs Q-headers |
