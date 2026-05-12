# [Debug hooks on the Python memory allocators](https://docs.python.org/3/c-api/memory.html#debug-hooks-on-the-python-memory-allocators)

Local notes on **Debug hooks on the Python memory allocators**, part of [*Memory Management*](https://docs.python.org/3/c-api/memory.html). This page summarizes patterns; authoritative text stays upstream.

- Follow the **[official section](https://docs.python.org/3/c-api/memory.html#debug-hooks-on-the-python-memory-allocators)** for exact signatures, deprecation notes, and edge cases.
- Most helpers advertise failures via `NULL` / `-1` and the **error indicator**; treat success paths carefully when references are borrowed vs new.
- Threading semantics are easy to violate in C extensions; skim the threading chapter alongside this section.

```c
#include <Python.h>

// Memory layers: prefer PyMem_Raw*/PyMem_* as documented for the lifetime you own;
// never mix allocators on the same pointer.
void *buf = PyMem_Malloc(64);
if (buf == NULL) {
    return PyErr_NoMemory();
}
PyMem_Free(buf);
```

Parent: [Memory Management](../index.md)
