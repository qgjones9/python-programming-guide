# [1.5. Compilation and Linkage](https://docs.python.org/3/extending/extending.html#compilation-and-linkage)

Local notes on **1.5. Compilation and Linkage** within [*1. Extending Python with C or C++*](https://docs.python.org/3/extending/extending.html).

- Detailed rules: **[1.5. Compilation and Linkage](https://docs.python.org/3/extending/extending.html#compilation-and-linkage)**.
- Companion reference: *[Python/C API Reference](../../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

Parent: [1. Extending Python with C or C++](../index.md)
