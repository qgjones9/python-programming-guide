# [4.1. Building C and C++ Extensions with setuptools](https://docs.python.org/3/extending/building.html#building-c-and-c-extensions-with-setuptools)

Local notes on **4.1. Building C and C++ Extensions with setuptools** within [*4. Building C and C++ Extensions*](https://docs.python.org/3/extending/building.html).

- Detailed rules: **[4.1. Building C and C++ Extensions with setuptools](https://docs.python.org/3/extending/building.html#building-c-and-c-extensions-with-setuptools)**.
- Companion reference: *[Python/C API Reference](../../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

Parent: [4. Building C and C++ Extensions](../index.md)
