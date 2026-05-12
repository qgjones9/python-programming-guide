# [Utilities](https://docs.python.org/3/c-api/utilities.html)

Local notes aligned with [**Utilities**](https://docs.python.org/3/c-api/utilities.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Operating System Utilities](https://docs.python.org/3/c-api/sys.html)

- Official docs: [Operating System Utilities](https://docs.python.org/3/c-api/sys.html) — behaviors, return values, and error conventions.
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

### [System Functions](https://docs.python.org/3/c-api/sys.html#system-functions)

- Official docs: [System Functions](https://docs.python.org/3/c-api/sys.html#system-functions) — behaviors, return values, and error conventions.
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

### [Process Control](https://docs.python.org/3/c-api/sys.html#process-control)

- Official docs: [Process Control](https://docs.python.org/3/c-api/sys.html#process-control) — behaviors, return values, and error conventions.
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

### [Importing Modules](https://docs.python.org/3/c-api/import.html)

- Official docs: [Importing Modules](https://docs.python.org/3/c-api/import.html) — behaviors, return values, and error conventions.
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

### [Data marshalling support](https://docs.python.org/3/c-api/marshal.html)

- Official docs: [Data marshalling support](https://docs.python.org/3/c-api/marshal.html) — behaviors, return values, and error conventions.
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

### [Parsing arguments and building values](https://docs.python.org/3/c-api/arg.html)

- Official docs: [Parsing arguments and building values](https://docs.python.org/3/c-api/arg.html) — behaviors, return values, and error conventions.
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

### [String conversion and formatting](https://docs.python.org/3/c-api/conversion.html)

- Official docs: [String conversion and formatting](https://docs.python.org/3/c-api/conversion.html) — behaviors, return values, and error conventions.
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

### [Character classification and conversion](https://docs.python.org/3/c-api/conversion.html#character-classification-and-conversion)

- Official docs: [Character classification and conversion](https://docs.python.org/3/c-api/conversion.html#character-classification-and-conversion) — behaviors, return values, and error conventions.
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

### [PyHash API](https://docs.python.org/3/c-api/hash.html)

- Official docs: [PyHash API](https://docs.python.org/3/c-api/hash.html) — behaviors, return values, and error conventions.
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

### [Reflection](https://docs.python.org/3/c-api/reflection.html)

- Official docs: [Reflection](https://docs.python.org/3/c-api/reflection.html) — behaviors, return values, and error conventions.
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

### [Codec registry and support functions](https://docs.python.org/3/c-api/codec.html)

- Official docs: [Codec registry and support functions](https://docs.python.org/3/c-api/codec.html) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

// Raising in C: use PyErr_SetString / PyErr_Format; return NULL or -1 as documented.
if (arg == NULL) {
    PyErr_SetString(PyExc_TypeError, "argument must not be NULL");
    return NULL;
}
```

### [PyTime C API](https://docs.python.org/3/c-api/time.html)

- Official docs: [PyTime C API](https://docs.python.org/3/c-api/time.html) — behaviors, return values, and error conventions.
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

### [Support for Perf Maps](https://docs.python.org/3/c-api/perfmaps.html)

- Official docs: [Support for Perf Maps](https://docs.python.org/3/c-api/perfmaps.html) — behaviors, return values, and error conventions.
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

## Sections in this repo

- [Operating System Utilities](operating-system-utilities/index.md)
- [System Functions](system-functions/index.md)
- [Process Control](process-control/index.md)
- [Importing Modules](importing-modules/index.md)
- [Data marshalling support](data-marshalling-support/index.md)
- [Parsing arguments and building values](parsing-arguments-and-building-values/index.md)
- [String conversion and formatting](string-conversion-and-formatting/index.md)
- [Character classification and conversion](character-classification-and-conversion/index.md)
- [PyHash API](pyhash-api/index.md)
- [Reflection](reflection/index.md)
- [Codec registry and support functions](codec-registry-and-support-functions/index.md)
- [PyTime C API](pytime-c-api/index.md)
- [Support for Perf Maps](support-for-perf-maps/index.md)
