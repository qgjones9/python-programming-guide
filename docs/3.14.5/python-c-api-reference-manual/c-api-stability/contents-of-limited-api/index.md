# [Contents of Limited API](https://docs.python.org/3/c-api/stable.html#contents-of-limited-api)

Local notes on **Contents of Limited API**, part of [*C API Stability*](https://docs.python.org/3/c-api/stable.html). This page summarizes patterns; authoritative text stays upstream.

- Follow the **[official section](https://docs.python.org/3/c-api/stable.html#contents-of-limited-api)** for exact signatures, deprecation notes, and edge cases.
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

Parent: [C API Stability](../index.md)
