# [API and ABI Versioning](https://docs.python.org/3/c-api/apiabiversion.html)

Local notes aligned with [**API and ABI Versioning**](https://docs.python.org/3/c-api/apiabiversion.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Build-time version constants](https://docs.python.org/3/c-api/apiabiversion.html#build-time-version-constants)

- Official docs: [Build-time version constants](https://docs.python.org/3/c-api/apiabiversion.html#build-time-version-constants) — behaviors, return values, and error conventions.
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

### [Run-time version](https://docs.python.org/3/c-api/apiabiversion.html#run-time-version)

- Official docs: [Run-time version](https://docs.python.org/3/c-api/apiabiversion.html#run-time-version) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

/* Reference borrowing vs new refs: borrowed pointers stay alive only while outer
 * invariants guarantee the owner is not mutated; call Py_INCREF if you stash them. */
PyObject *borrowed = PyTuple_GET_ITEM(tuple_arg, 0);  /* borrowed from tuple */
Py_INCREF(borrowed);
/* ... stash borrowed where needed ... */
Py_DECREF(borrowed);
```

### [Bit-packing macros](https://docs.python.org/3/c-api/apiabiversion.html#bit-packing-macros)

- Official docs: [Bit-packing macros](https://docs.python.org/3/c-api/apiabiversion.html#bit-packing-macros) — behaviors, return values, and error conventions.
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

## Sections in this repo

- [Build-time version constants](build-time-version-constants/index.md)
- [Run-time version](run-time-version/index.md)
- [Bit-packing macros](bit-packing-macros/index.md)
