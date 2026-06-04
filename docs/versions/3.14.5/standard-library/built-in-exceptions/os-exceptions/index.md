# [OS exceptions](https://docs.python.org/3/library/exceptions.html#os-exceptions)

Since Python 3.3 (PEP 3151), operating-system and I/O failures share a single hierarchy rooted at [`OSError`](../concrete-exceptions/oserror/index.md). When the C `errno` value is known, constructing `OSError` directly—or letting the interpreter raise it from a syscall—often yields a **more specific subclass** such as `FileNotFoundError` or `ConnectionRefusedError`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#os-exceptions); this page explains the hierarchy, errno mapping, and practical handling patterns.

---

## Hierarchy overview

All types in this section inherit from `OSError`, which itself inherits from [`Exception`](../base-classes/exception/index.md). `ConnectionError` is an intermediate base for socket and pipe failures; filesystem-oriented types (`FileNotFoundError`, `PermissionError`, …) inherit directly from `OSError`.

```python
# Goal: confirm the OS exception tree matches PEP 3151
assert issubclass(FileNotFoundError, OSError)
assert issubclass(PermissionError, OSError)
assert issubclass(ConnectionError, OSError)
assert issubclass(BrokenPipeError, ConnectionError)
assert issubclass(ConnectionRefusedError, ConnectionError)
assert issubclass(OSError, Exception)
```

| Layer | Types |
|-------|-------|
| Root | [`OSError`](../concrete-exceptions/oserror/index.md) |
| Connection family | [`ConnectionError`](connectionerror/index.md) → `BrokenPipeError`, `ConnectionAbortedError`, `ConnectionRefusedError`, `ConnectionResetError` |
| Filesystem / process | `BlockingIOError`, `ChildProcessError`, `FileExistsError`, `FileNotFoundError`, `InterruptedError`, `IsADirectoryError`, `NotADirectoryError`, `PermissionError`, `ProcessLookupError`, `TimeoutError` |

Legacy names `EnvironmentError`, `IOError`, and (on Windows) `WindowsError` are aliases of `OSError` since 3.3.

---

## Automatic subclass selection

When you call `OSError(errno, strerror, …)` or receive an OS failure from the interpreter, CPython maps the numeric `errno` to the appropriate subclass. This behaviour applies to **direct** `OSError` construction and aliases—not to user-defined subclasses of `OSError`.

```python
import errno

# Goal: errno codes map to the documented subclasses
mapping = [
    (errno.ENOENT, FileNotFoundError),
    (errno.EEXIST, FileExistsError),
    (errno.EACCES, PermissionError),
    (errno.ETIMEDOUT, TimeoutError),
    (errno.EPIPE, BrokenPipeError),
    (errno.ECONNREFUSED, ConnectionRefusedError),
    (errno.ECONNRESET, ConnectionResetError),
    (errno.EINTR, InterruptedError),
    (errno.EISDIR, IsADirectoryError),
    (errno.ENOTDIR, NotADirectoryError),
]
for code, expected in mapping:
    exc = OSError(code, "demo")
    assert isinstance(exc, expected), (code, type(exc).__name__)
```

### errno → exception mapping {#errno--exception-mapping}

| errno constant(s) | Exception |
|-------------------|-----------|
| `EAGAIN`, `EALREADY`, `EWOULDBLOCK`, `EINPROGRESS` | [`BlockingIOError`](blockingioerror/index.md) |
| `ECHILD` | [`ChildProcessError`](childprocesserror/index.md) |
| `EPIPE`, `ESHUTDOWN` | [`BrokenPipeError`](brokenpipeerror/index.md) |
| `ECONNABORTED` | [`ConnectionAbortedError`](connectionabortederror/index.md) |
| `ECONNREFUSED` | [`ConnectionRefusedError`](connectionrefusederror/index.md) |
| `ECONNRESET` | [`ConnectionResetError`](connectionreseterror/index.md) |
| `EEXIST` | [`FileExistsError`](fileexistserror/index.md) |
| `ENOENT` | [`FileNotFoundError`](filenotfounderror/index.md) |
| `EINTR` | [`InterruptedError`](interruptederror/index.md) |
| `EISDIR` | [`IsADirectoryError`](isadirectoryerror/index.md) |
| `ENOTDIR` | [`NotADirectoryError`](notadirectoryerror/index.md) |
| `EACCES`, `EPERM`, `ENOTCAPABLE` | [`PermissionError`](permissionerror/index.md) |
| `ESRCH` | [`ProcessLookupError`](processlookuperror/index.md) |
| `ETIMEDOUT` | [`TimeoutError`](timeouterror/index.md) |

Unlisted errno values remain plain `OSError`. On Windows, the constructor may also accept `winerror`; `errno` is then derived from the native code when possible.

---

## `OSError` attributes

Every instance (including subclasses) exposes syscall context on attributes—not only in the message string:

| Attribute | Meaning |
|-----------|---------|
| `errno` | Numeric error code from C `errno` (POSIX-style). |
| `strerror` | Human-readable message from the OS (`perror` / `FormatMessage`). |
| `filename` | Path argument for single-path operations (`open`, `os.unlink`, …). |
| `filename2` | Second path for two-path operations (`os.rename`, …). |
| `winerror` | Native Windows error code (Windows only). |

```python
import errno

exc = OSError(errno.ENOENT, "No such file", "/tmp/missing.txt")
assert exc.errno == errno.ENOENT
assert exc.strerror == "No such file"
assert exc.filename == "/tmp/missing.txt"
assert isinstance(exc, FileNotFoundError)
```

---

## EAFP vs LBYL

Python idioms prefer **EAFP** (Easier to Ask Forgiveness than Permission): attempt the operation and catch the specific `OSError` subclass. **LBYL** (Look Before You Leap)—testing with `os.path.exists` or similar before opening—can race when another process deletes or creates the path between the check and the use.

```python
import os
import tempfile

def read_text_eafp(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""

def read_text_lbyl(path):
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()
    return ""

missing = os.path.join(tempfile.gettempdir(), "pguide-eafp-demo-missing")
assert read_text_eafp(missing) == ""
assert read_text_lbyl(missing) == ""
```

Prefer `except FileNotFoundError` over bare `except OSError` when you only want “missing file,” and `except PermissionError` when access is denied—subclass handlers still satisfy `except OSError` because matching walks the inheritance tree.

---

## Best practices for file and network code

| Situation | Recommendation |
|-----------|------------------|
| Missing config / optional file | Catch `FileNotFoundError`; return a default or create the file. |
| “Already exists” on create | Catch `FileExistsError` or use `exist_ok=True` / atomic flags where the API supports them. |
| Broad network retry | Catch [`ConnectionError`](connectionerror/index.md) for transient peer failures; inspect `type(exc).__name__` or `exc.errno` for logging. |
| Timeouts | Catch `TimeoutError` (system-level) separately from [`TimeoutError`](timeouterror/index.md) in `concurrent.futures` (same name, different modules—use qualified imports in mixed code). |
| Cleanup in `finally` | Ignore `FileNotFoundError` on `os.remove`; do not swallow `PermissionError` silently. |
| Logging | Log `exc.errno`, `exc.strerror`, and `exc.filename` (or `exc.args`) for support tickets. |

```python
def remove_if_present(path):
    try:
        import os
        os.remove(path)
    except FileNotFoundError:
        pass  # already gone — goal met

remove_if_present("/tmp/almost-certainly-not-there-pguide")
```

---

## Platform notes

| Topic | Detail |
|-------|--------|
| PEP 3151 | Unified `OSError` hierarchy; added all errno-specific subclasses in 3.3. |
| PEP 475 | Since 3.5, interrupted syscalls are **retried** automatically; bare `EINTR` → `InterruptedError` is rare in application code unless a signal handler raises. |
| Windows | `winerror` attribute and approximate POSIX `errno`; see [`WindowsError`](../concrete-exceptions/windowserror/index.md) alias. |
| WASI | `ENOTCAPABLE` maps to `PermissionError` since 3.11.1. |
| Non-blocking I/O | [`BlockingIOError`](blockingioerror/index.md) may include `characters_written` from buffered streams. |

---

## Table of contents

Mirrors the official Python 3 library index for this section. Each link opens an enriched page whose H1 links to the canonical docs.

| Exception | Description |
|-----------|-------------|
| [BlockingIOError](blockingioerror/index.md) | Raised when an operation would block on an object (e.g. socket) set for non-blocking operation. Corresponds to errno EAGAIN, EALREADY, EWOULDBLOCK and EINPROGRESS. |
| [ChildProcessError](childprocesserror/index.md) | Raised when an operation on a child process failed. Corresponds to errno ECHILD. |
| [ConnectionError](connectionerror/index.md) | Base class for connection-related issues; subclasses include BrokenPipeError, ConnectionAbortedError, ConnectionRefusedError, and ConnectionResetError. |
| [BrokenPipeError](brokenpipeerror/index.md) | Subclass of ConnectionError, raised when writing on a closed pipe or a socket shut down for writing. Corresponds to errno EPIPE and ESHUTDOWN. |
| [ConnectionAbortedError](connectionabortederror/index.md) | Subclass of ConnectionError, raised when a connection attempt is aborted by the peer. Corresponds to errno ECONNABORTED. |
| [ConnectionRefusedError](connectionrefusederror/index.md) | Subclass of ConnectionError, raised when a connection attempt is refused by the peer. Corresponds to errno ECONNREFUSED. |
| [ConnectionResetError](connectionreseterror/index.md) | Subclass of ConnectionError, raised when a connection is reset by the peer. Corresponds to errno ECONNRESET. |
| [FileExistsError](fileexistserror/index.md) | Raised when trying to create a file or directory that already exists. Corresponds to errno EEXIST. |
| [FileNotFoundError](filenotfounderror/index.md) | Raised when a requested file or directory does not exist. Corresponds to errno ENOENT. |
| [InterruptedError](interruptederror/index.md) | Raised when a system call is interrupted by an incoming signal. Corresponds to errno EINTR. |
| [IsADirectoryError](isadirectoryerror/index.md) | Raised when a file operation (such as os.remove()) is requested on a directory. Corresponds to errno EISDIR. |
| [NotADirectoryError](notadirectoryerror/index.md) | Raised when a directory operation (such as os.listdir()) is requested on something that is not a directory. Corresponds to errno ENOTDIR. |
| [PermissionError](permissionerror/index.md) | Raised when an operation lacks adequate access rights (e.g. filesystem permissions). Corresponds to errno EACCES, EPERM, and ENOTCAPABLE. |
| [ProcessLookupError](processlookuperror/index.md) | Raised when a given process does not exist. Corresponds to errno ESRCH. |
| [TimeoutError](timeouterror/index.md) | Raised when a system function timed out at the system level. Corresponds to errno ETIMEDOUT. |

---

## Sections in this repo

Child pages for each errno-specific `OSError` subclass:

- [BlockingIOError](blockingioerror/index.md)
- [BrokenPipeError](brokenpipeerror/index.md)
- [ChildProcessError](childprocesserror/index.md)
- [ConnectionAbortedError](connectionabortederror/index.md)
- [ConnectionError](connectionerror/index.md)
- [ConnectionRefusedError](connectionrefusederror/index.md)
- [ConnectionResetError](connectionreseterror/index.md)
- [FileExistsError](fileexistserror/index.md)
- [FileNotFoundError](filenotfounderror/index.md)
- [InterruptedError](interruptederror/index.md)
- [IsADirectoryError](isadirectoryerror/index.md)
- [NotADirectoryError](notadirectoryerror/index.md)
- [PermissionError](permissionerror/index.md)
- [ProcessLookupError](processlookuperror/index.md)
- [TimeoutError](timeouterror/index.md)

Parent type: [`OSError`](../concrete-exceptions/oserror/index.md).
