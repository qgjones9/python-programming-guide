# [1.4. The Module’s Method Table and Initialization Function](https://docs.python.org/3/extending/extending.html#the-module-s-method-table-and-initialization-function)

Local notes on **1.4. The Module’s Method Table and Initialization Function** within [*1. Extending Python with C or C++*](https://docs.python.org/3/extending/extending.html).

- Detailed rules: **[1.4. The Module’s Method Table and Initialization Function](https://docs.python.org/3/extending/extending.html#the-module-s-method-table-and-initialization-function)**.
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
