# [1.6. Compiling and Linking under Unix-like systems](https://docs.python.org/3/extending/embedding.html#compiling-and-linking-under-unix-like-systems)

Local notes on **1.6. Compiling and Linking under Unix-like systems** within [*1. Embedding Python in Another Application*](https://docs.python.org/3/extending/embedding.html).

- Detailed rules: **[1.6. Compiling and Linking under Unix-like systems](https://docs.python.org/3/extending/embedding.html#compiling-and-linking-under-unix-like-systems)**.
- Companion reference: *[Python/C API Reference](../../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Minimal PyInit prototype; publish methods via PyMethodDef/PyModuleDef (see guide). */
static PyMethodDef _methods[] = {
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef _mod = {
    PyModuleDef_HEAD_INIT, "demo", NULL, -1, _methods,
};

PyMODINIT_FUNC
PyInit_demo(void)
{
    return PyModule_Create(&_mod);
}
```

Parent: [1. Embedding Python in Another Application](../index.md)
