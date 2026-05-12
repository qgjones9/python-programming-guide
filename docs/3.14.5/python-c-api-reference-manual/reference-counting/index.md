# [Reference Counting](https://docs.python.org/3/c-api/refcounting.html)

Single-page chapter in [**Reference Counting**](https://docs.python.org/3/c-api/refcounting.html); no subdivisions below in this mirror.
Skim overview bullets here, follow the canonical link for the full narrative and API listings.

- Canonical: [Reference Counting](https://docs.python.org/3/c-api/refcounting.html)
- Treat return codes and refcount contracts exactly as documented; many helpers set the error indicator instead of asserting.
- Threading nuances (where applicable) belong to this chapter and may depend on `_Py` internals for debug builds.

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
