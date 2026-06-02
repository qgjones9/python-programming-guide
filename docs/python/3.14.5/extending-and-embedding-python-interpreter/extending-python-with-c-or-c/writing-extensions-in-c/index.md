# [1.11. Writing Extensions in C++](https://docs.python.org/3/extending/extending.html#writing-extensions-in-c)

Local notes on **1.11. Writing Extensions in C++** within [*1. Extending Python with C or C++*](https://docs.python.org/3/extending/extending.html).

- Detailed rules: **[1.11. Writing Extensions in C++](https://docs.python.org/3/extending/extending.html#writing-extensions-in-c)**.
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

Parent: [1. Extending Python with C or C++](../index.md)
