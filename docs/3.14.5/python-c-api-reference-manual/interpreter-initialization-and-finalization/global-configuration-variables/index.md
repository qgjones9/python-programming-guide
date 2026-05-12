# [Global configuration variables](https://docs.python.org/3/c-api/interp-lifecycle.html#global-configuration-variables)

Local notes on **Global configuration variables**, part of [*Interpreter initialization and finalization*](https://docs.python.org/3/c-api/interp-lifecycle.html). This page summarizes patterns; authoritative text stays upstream.

- Follow the **[official section](https://docs.python.org/3/c-api/interp-lifecycle.html#global-configuration-variables)** for exact signatures, deprecation notes, and edge cases.
- Most helpers advertise failures via `NULL` / `-1` and the **error indicator**; treat success paths carefully when references are borrowed vs new.
- Threading semantics are easy to violate in C extensions; skim the threading chapter alongside this section.

```c
#include <Python.h>

// Raising in C: use PyErr_SetString / PyErr_Format; return NULL or -1 as documented.
if (arg == NULL) {
    PyErr_SetString(PyExc_TypeError, "argument must not be NULL");
    return NULL;
}
```

Parent: [Interpreter initialization and finalization](../index.md)
