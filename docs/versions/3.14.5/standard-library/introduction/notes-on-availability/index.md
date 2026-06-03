# [Notes on availability](https://docs.python.org/3.14/library/intro.html#notes-on-availability)

Many standard library modules and functions document an **Availability** line. This page explains how to read those notes and what to expect on WebAssembly and mobile ports. Full prose lives on [docs.python.org](https://docs.python.org/3.14/library/intro.html#notes-on-availability).

### Unix availability — [Notes on availability](https://docs.python.org/3.14/library/intro.html#notes-on-availability)

- **“Availability: Unix”** means the API is *commonly* found on Unix-like systems—not a guarantee on every OS or build.
- Unless noted otherwise, **“Availability: Unix”** also covers **macOS**, **iOS**, and **Android** (all build on a Unix core).
- When a note lists **both** a minimum kernel version and a minimum **libc** version, **both** must be satisfied.

| Note example | Meaning |
|--------------|---------|
| `Availability: Unix` | Typical on Unix-like systems; includes macOS, iOS, Android unless stated otherwise |
| `Availability: Linux >= 3.17 with glibc >= 2.27` | Requires Linux **3.17+** **and** glibc **2.27+** |

```python
import sys

# Platform string helps interpret availability notes in docs
print(sys.platform)  # e.g. 'linux', 'darwin', 'android', 'ios', 'wasm32-emscripten'
```

### WebAssembly platforms — [WebAssembly platforms](https://docs.python.org/3.14/library/intro.html#webassembly-platforms)

Targets **`wasm32-emscripten`** (Emscripten) and **`wasm32-wasi`** (WASI) expose only a **subset** of POSIX APIs. Runtimes and browsers are sandboxed, so process control, threading, networking, signals, and IPC often differ from desktop Unix.

| Area | Behavior on WebAssembly |
|------|-------------------------|
| Processes / IPC | APIs such as `fork()`, `execve()`, `waitpid()`, `kill()` are unavailable or always fail; [`subprocess`](../../concurrent-execution/subprocess-subprocess-management/index.md) imports but does not work |
| Blocking I/O | Emscripten disallows blocking I/O; blocking calls like `time.sleep()` can block the browser event loop |
| [`socket`](../../networking-and-interprocess-communication/socket-low-level-networking-interface/index.md) | Present but limited; Emscripten sockets are non-blocking and may need WebSocket proxying; WASI preview 1 allows sockets only from an existing file descriptor |
| File descriptors / permissions / links | Restricted; some calls are stubs; WASI forbids absolute-path symlinks |
| Evolution | Behavior depends on Emscripten/WASI SDK, runtime (browser, Node.js, wasmtime), and build flags |

For Python in the browser, consider **[Pyodide](https://pyodide.org/en/stable/)** or **[PyScript](https://pyscript.net/)** (PyScript builds on Pyodide). Pyodide exposes JavaScript/DOM APIs and limited networking via `XMLHttpRequest` and `Fetch`.

### Mobile platforms — [Mobile platforms](https://docs.python.org/3.14/library/intro.html#mobile-platforms)

Android and iOS are mostly POSIX for file I/O, sockets, and threading, but mobile embedding differs sharply from desktop CPython.

| Topic | Android | iOS |
|-------|---------|-----|
| Deployment | Embedded mode only—no standalone `python`/`pip` REPL; use the [embedding API](https://docs.python.org/3/extending/embedding.html) | Same; see [Using Python on Android](https://docs.python.org/3/using/android.html) and [Using Python on iOS](https://docs.python.org/3/using/ios.html) |
| Subprocesses / multiprocessing | Possible but **unsupported**; no System V IPC → no `multiprocessing` | **Not allowed**—subprocess/IPC can hang or crash; no visibility into other apps except via iOS APIs |
| System resources | Often readable; writes (e.g. system clock) usually fail | Same pattern |
| `stdout` / `stderr` | Native streams disconnected; Python redirects to log tags `python.stdout` / `python.stderr` | Visible in Xcode logs; **not** in system log users can export |
| `stdin` | No usable stdin (on-screen keyboard is not stdin) | Same |
| Console modules | [`curses`](../../command-line-interface-libraries/curses-terminal-handling-for-character-cell-displays/index.md) and [`readline`](../../text-processing-services/readline-gnu-readline-interface/index.md) unavailable | Same |
