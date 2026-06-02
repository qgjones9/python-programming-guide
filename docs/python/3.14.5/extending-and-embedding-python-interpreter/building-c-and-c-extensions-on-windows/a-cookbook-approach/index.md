# [5.1. A Cookbook Approach](https://docs.python.org/3/extending/windows.html#a-cookbook-approach)

Local notes on **5.1. A Cookbook Approach** within [*5. Building C and C++ Extensions on Windows*](https://docs.python.org/3/extending/windows.html).

- Detailed rules: **[5.1. A Cookbook Approach](https://docs.python.org/3/extending/windows.html#a-cookbook-approach)**.
- Companion reference: *[Python/C API Reference](../../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

Parent: [5. Building C and C++ Extensions on Windows](../index.md)
