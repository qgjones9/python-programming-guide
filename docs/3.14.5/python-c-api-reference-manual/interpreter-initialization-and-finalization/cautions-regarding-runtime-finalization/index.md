# [Cautions regarding runtime finalization](https://docs.python.org/3/c-api/interp-lifecycle.html#cautions-regarding-runtime-finalization)

Local notes on **Cautions regarding runtime finalization**, part of [*Interpreter initialization and finalization*](https://docs.python.org/3/c-api/interp-lifecycle.html). This page summarizes patterns; authoritative text stays upstream.

- Follow the **[official section](https://docs.python.org/3/c-api/interp-lifecycle.html#cautions-regarding-runtime-finalization)** for exact signatures, deprecation notes, and edge cases.
- Most helpers advertise failures via `NULL` / `-1` and the **error indicator**; treat success paths carefully when references are borrowed vs new.
- Threading semantics are easy to violate in C extensions; skim the threading chapter alongside this section.

```c
#include <Python.h>

// When holding the GIL, most object APIs expect the main interpreter state;
// embedding code must bracket calls appropriately (see official section on threads).
PyGILState_STATE gstate = PyGILState_Ensure();
(void)PyRun_SimpleStringFlags("pass\n", NULL);
PyGILState_Release(gstate);
```

Parent: [Interpreter initialization and finalization](../index.md)
