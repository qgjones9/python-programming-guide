# [Multi-phase initialization](https://docs.python.org/3/c-api/extension-modules.html#multi-phase-initialization)

Local notes on **Multi-phase initialization**, part of [*Defining extension modules*](https://docs.python.org/3/c-api/extension-modules.html). This page summarizes patterns; authoritative text stays upstream.

- Follow the **[official section](https://docs.python.org/3/c-api/extension-modules.html#multi-phase-initialization)** for exact signatures, deprecation notes, and edge cases.
- Most helpers advertise failures via `NULL` / `-1` and the **error indicator**; treat success paths carefully when references are borrowed vs new.
- Threading semantics are easy to violate in C extensions; skim the threading chapter alongside this section.

```c
#include <Python.h>

/* Reference borrowing vs new refs: borrowed pointers stay alive only while outer
 * invariants guarantee the owner is not mutated; call Py_INCREF if you stash them. */
PyObject *borrowed = PyTuple_GET_ITEM(tuple_arg, 0);  /* borrowed from tuple */
Py_INCREF(borrowed);
/* ... stash borrowed where needed ... */
Py_DECREF(borrowed);
```

Parent: [Defining extension modules](../index.md)
