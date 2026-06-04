# [ctypes — A foreign function library for Python](https://docs.python.org/3/library/ctypes.html)

The [`ctypes`](https://docs.python.org/3/library/ctypes.html) module loads **shared libraries** (`.so`, `.dll`, `.dylib`) and calls C functions from pure Python — no C extension compile step. Define **`Structure`** layouts, **`POINTER`** types, and **`CFUNCTYPE`** callbacks; set **`argtypes`** and **`restype`** on function pointers for safety. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/ctypes.html).

Related: [`struct`](../../binary-data-services/struct-python-bytes-objects/index.md) for pure-Python packing; C extension docs for production FFI; [`os`](../os-miscellaneous-operating-system-interfaces/index.md) for loading paths.

**Safety note:** incorrect prototypes can crash the interpreter; prefer [`cffi`](https://cffi.readthedocs.io/) or a compiled extension for complex APIs.

---

## Core concepts — overview

| Concept | Role |
|---------|------|
| `CDLL` / `WinDLL` / `OleDLL` | Load library, call functions with cdecl/stdcall |
| `c_int`, `c_void_p`, … | Scalar C types |
| `Structure` / `Union` | C struct memory layout |
| `POINTER(T)` | Pointer types |
| `byref(x)` / `pointer(x)` | Pass by reference |
| `CFUNCTYPE` / `WINFUNCTYPE` | Python callable as C function pointer |
| `create_string_buffer` | Writable char buffer |

---

## Loading libraries — [Loading dynamic link libraries](https://docs.python.org/3/library/ctypes.html#loading-dynamic-link-libraries)

| API | Notes |
|-----|-------|
| `ctypes.CDLL(name)` | cdecl calling convention (Unix default) |
| `ctypes.WinDLL(name)` | stdcall on Windows |
| `ctypes.pythonapi` | Preloaded Python C API |
| `ctypes.util.find_library(name)` | Locate library basename (platform-dependent) |

Always set **`restype`** and **`argtypes`** after resolving a function.

---

## Structures and callbacks

```python
# Goal: define a C struct and read fields
import ctypes

class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]

p = Point(3, 4)
assert p.x == 3 and p.y == 4
assert ctypes.sizeof(Point) >= 8
```

```python
# Goal: Python function as C callback
import ctypes

@ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)
def add(a, b):
    return a + b

assert add(2, 3) == 5
```

```python
# Goal: pack/unpack with native byte order
import ctypes

class Header(ctypes.Structure):
    _fields_ = [("magic", ctypes.c_uint32), ("count", ctypes.c_uint16)]

h = Header(magic=0xCAFE, count=42)
raw = bytes(ctypes.string_at(ctypes.byref(h), ctypes.sizeof(h)))
clone = Header.from_buffer_copy(raw)
assert clone.magic == 0xCAFE and clone.count == 42
```

---

## String buffers — [Working with pointers](https://docs.python.org/3/library/ctypes.html)

| API | Role |
|-----|------|
| `create_string_buffer(n)` | Writable bytes buffer |
| `c_char_p` | `char*` (immutable string pointer) |
| `string_at(ptr, size=-1)` | Read bytes from address |

---

## Best practices

| Practice | Why |
|----------|-----|
| Set **`argtypes`/`restype`** on every function | Prevents stack corruption |
| Match **`Structure._pack_`** to C header | Alignment mismatches corrupt fields |
| Use **`bytes`** for `c_char_p` input | Avoid implicit encoding surprises |
| Keep **callbacks alive** | GC collects unused CFUNCTYPE wrappers → crash |
| Prefer **`from_buffer_copy`** for snapshots | Avoid aliasing mutable memory unintentionally |
| Test on **target ABI** (32 vs 64 bit) | Pointer sizes differ |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Wrong **`restype`** | Garbage return values | Match C declaration exactly |
| **`c_char_p` to mutable buffer** | C keeps pointer to freed memory | Use `create_string_buffer` |
| **`bool` vs `c_int`** | C `_Bool` vs int mismatch | Use `c_bool` when header says so |
| **`CDLL(None)`** portability | Not available everywhere | Load explicit library name |
| **GIL and callbacks** | Re-enter Python from C thread | Follow callback threading rules upstream |
| **Bit fields in Structure** | Platform-dependent layout | Avoid or mirror compiler exactly |

---

## ctypes vs alternatives

| Tool | Trade-off |
|------|-----------|
| `ctypes` | Stdlib, quick probes; easy to crash |
| `cffi` | Safer parsing of C declarations; extra dependency |
| C extension | Best performance and correctness; compile required |
