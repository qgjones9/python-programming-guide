# [The Very High Level Layer](https://docs.python.org/3/c-api/veryhigh.html)

Local notes aligned with [**The Very High Level Layer**](https://docs.python.org/3/c-api/veryhigh.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Available start symbols](https://docs.python.org/3/c-api/veryhigh.html#available-start-symbols)

- Official docs: [Available start symbols](https://docs.python.org/3/c-api/veryhigh.html#available-start-symbols) — behaviors, return values, and error conventions.
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

### [Stack Effects](https://docs.python.org/3/c-api/veryhigh.html#stack-effects)

- Official docs: [Stack Effects](https://docs.python.org/3/c-api/veryhigh.html#stack-effects) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

// Many C APIs return either a pointer or NULL; NULL means failure and the error
// indicator may be set (check with PyErr_Occurred()). Clear or propagate when appropriate.
PyObject *value = PyLong_FromLong(2026);
if (value == NULL) {
    return NULL;  /* let the interpreter surface the pending exception */
}
Py_DECREF(value);
```

## Sections in this repo

- [Available start symbols](available-start-symbols/index.md)
- [Stack Effects](stack-effects/index.md)
