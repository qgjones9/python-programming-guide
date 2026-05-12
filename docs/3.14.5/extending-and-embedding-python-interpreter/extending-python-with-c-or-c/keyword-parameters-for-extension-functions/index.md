# [1.8. Keyword Parameters for Extension Functions](https://docs.python.org/3/extending/extending.html#keyword-parameters-for-extension-functions)

Local notes on **1.8. Keyword Parameters for Extension Functions** within [*1. Extending Python with C or C++*](https://docs.python.org/3/extending/extending.html).

- Detailed rules: **[1.8. Keyword Parameters for Extension Functions](https://docs.python.org/3/extending/extending.html#keyword-parameters-for-extension-functions)**.
- Companion reference: *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

Parent: [1. Extending Python with C or C++](../index.md)
