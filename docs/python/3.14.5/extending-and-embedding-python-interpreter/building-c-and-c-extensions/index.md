# [4. Building C and C++ Extensions](https://docs.python.org/3/extending/building.html)

Scratch notes backing [**4. Building C and C++ Extensions**](https://docs.python.org/3/extending/building.html) inside *[Extending and Embedding](https://docs.python.org/3/extending/index.html#extending-index)*.

### [4.1. Building C and C++ Extensions with setuptools](https://docs.python.org/3/extending/building.html#building-c-and-c-extensions-with-setuptools)

- Full write-up: [4.1. Building C and C++ Extensions with setuptools](https://docs.python.org/3/extending/building.html#building-c-and-c-extensions-with-setuptools).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

## Sections in this repo

- [4.1. Building C and C++ Extensions with setuptools](building-c-and-c-extensions-with-setuptools/index.md)
