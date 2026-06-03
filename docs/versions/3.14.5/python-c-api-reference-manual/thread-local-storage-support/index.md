# [Thread-local storage support](https://docs.python.org/3/c-api/tls.html)

Local notes aligned with [**Thread-local storage support**](https://docs.python.org/3/c-api/tls.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Thread-specific storage API](https://docs.python.org/3/c-api/tls.html#thread-specific-storage-api)

- Official docs: [Thread-specific storage API](https://docs.python.org/3/c-api/tls.html#thread-specific-storage-api) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

// When holding the GIL, most object APIs expect the main interpreter state;
// embedding code must bracket calls appropriately (see official section on threads).
PyGILState_STATE gstate = PyGILState_Ensure();
(void)PyRun_SimpleStringFlags("pass\n", NULL);
PyGILState_Release(gstate);
```

### [Dynamic allocation](https://docs.python.org/3/c-api/tls.html#dynamic-allocation)

- Official docs: [Dynamic allocation](https://docs.python.org/3/c-api/tls.html#dynamic-allocation) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

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

### [Methods](https://docs.python.org/3/c-api/tls.html#methods)

- Official docs: [Methods](https://docs.python.org/3/c-api/tls.html#methods) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

// When holding the GIL, most object APIs expect the main interpreter state;
// embedding code must bracket calls appropriately (see official section on threads).
PyGILState_STATE gstate = PyGILState_Ensure();
(void)PyRun_SimpleStringFlags("pass\n", NULL);
PyGILState_Release(gstate);
```

### [Legacy APIs](https://docs.python.org/3/c-api/tls.html#legacy-apis)

- Official docs: [Legacy APIs](https://docs.python.org/3/c-api/tls.html#legacy-apis) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

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

## Sections in this repo

- [Thread-specific storage API](thread-specific-storage-api/index.md)
- [Dynamic allocation](dynamic-allocation/index.md)
- [Methods](methods/index.md)
- [Legacy APIs](legacy-apis/index.md)
