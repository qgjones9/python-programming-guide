# [ftplib — FTP protocol client](https://docs.python.org/3/library/ftplib.html)

[`ftplib`](https://docs.python.org/3/library/ftplib.html) implements an **FTP client** (`FTP`, `FTP_TLS`): login, cwd, nlst/dir, retrbinary/storbinary transfers, and passive/active mode helpers. FTP sends credentials in cleartext unless wrapped in **`FTP_TLS`**. Reference: [ftplib](https://docs.python.org/3/library/ftplib.html).

---

## Typical session methods

| Method | Role |
|--------|------|
| `ftp.connect(host, port=21)` | Open control connection |
| `ftp.login(user, passwd)` | Authenticate |
| `ftp.retrbinary('RETR name', callback)` | Download binary file |
| `ftp.storbinary('STOR name', file)` | Upload binary file |
| `ftp.quit()` | Graceful shutdown |

---

## Example — parse passive-mode response offline

```python
# Goal: decode PASV response host/port without live FTP server
import ftplib

line = "227 Entering Passive Mode (127,0,0,1,195,149)."
host, port = ftplib.parse227(line)
assert host == "127.0.0.1"
assert port == 195 * 256 + 149

assert ftplib.error_perm.__name__ == "error_perm"
```

---

## Security

| Risk | Mitigation |
|------|------------|
| Cleartext credentials | Use `FTP_TLS` with verified TLS context |
| Legacy protocol | Prefer SFTP/HTTPS for new designs |

Exception classes: `error_temp`, `error_perm`, `error_proto`, `error_reply`.
