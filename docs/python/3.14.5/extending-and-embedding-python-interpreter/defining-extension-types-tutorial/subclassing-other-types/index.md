# [2.5. Subclassing other types](https://docs.python.org/3/extending/newtypes_tutorial.html#subclassing-other-types)

Local notes on **2.5. Subclassing other types** within [*2. Defining Extension Types: Tutorial*](https://docs.python.org/3/extending/newtypes_tutorial.html).

- Detailed rules: **[2.5. Subclassing other types](https://docs.python.org/3/extending/newtypes_tutorial.html#subclassing-other-types)**.
- Companion reference: *[Python/C API Reference](../../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

Parent: [2. Defining Extension Types: Tutorial](../index.md)
