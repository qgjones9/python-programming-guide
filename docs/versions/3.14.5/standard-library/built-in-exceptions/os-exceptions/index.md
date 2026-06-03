# [OS exceptions](https://docs.python.org/3/library/exceptions.html#os-exceptions)

The following exceptions are subclasses of OSError; they get raised depending on the system error code.

## Table of contents

Mirrors the official Python 3 library index for this section. Each link opens a stub page whose H1 links to the canonical docs.

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
