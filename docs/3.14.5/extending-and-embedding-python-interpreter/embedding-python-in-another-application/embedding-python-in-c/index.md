# [1.5. Embedding Python in C++](https://docs.python.org/3/extending/embedding.html#embedding-python-in-c)

Local notes on **1.5. Embedding Python in C++** within [*1. Embedding Python in Another Application*](https://docs.python.org/3/extending/embedding.html).

- Detailed rules: **[1.5. Embedding Python in C++](https://docs.python.org/3/extending/embedding.html#embedding-python-in-c)**.
- Companion reference: *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

Parent: [1. Embedding Python in Another Application](../index.md)
