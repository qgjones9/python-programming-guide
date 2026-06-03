# [Profiling and tracing](https://docs.python.org/3/c-api/profiling.html)

Single-page chapter in [**Profiling and tracing**](https://docs.python.org/3/c-api/profiling.html); no subdivisions below in this mirror.
Skim overview bullets here, follow the canonical link for the full narrative and API listings.

- Canonical: [Profiling and tracing](https://docs.python.org/3/c-api/profiling.html)
- Treat return codes and refcount contracts exactly as documented; many helpers set the error indicator instead of asserting.
- Threading nuances (where applicable) belong to this chapter and may depend on `_Py` internals for debug builds.

```c
#include <Python.h>

/* Reference borrowing vs new refs: borrowed pointers stay alive only while outer
 * invariants guarantee the owner is not mutated; call Py_INCREF if you stash them. */
PyObject *borrowed = PyTuple_GET_ITEM(tuple_arg, 0);  /* borrowed from tuple */
Py_INCREF(borrowed);
/* ... stash borrowed where needed ... */
Py_DECREF(borrowed);
```
