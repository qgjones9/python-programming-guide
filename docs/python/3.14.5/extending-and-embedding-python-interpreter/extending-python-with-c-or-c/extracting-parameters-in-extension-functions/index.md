# [1.7. Extracting Parameters in Extension Functions](https://docs.python.org/3/extending/extending.html#extracting-parameters-in-extension-functions)

Local notes on **1.7. Extracting Parameters in Extension Functions** within [*1. Extending Python with C or C++*](https://docs.python.org/3/extending/extending.html).

- Detailed rules: **[1.7. Extracting Parameters in Extension Functions](https://docs.python.org/3/extending/extending.html#extracting-parameters-in-extension-functions)**.
- Companion reference: *[Python/C API Reference](../../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Returned PyObject pointers are usually new refs—pair Py_DECREF once done. */
PyObject *tmp = PyLong_FromLong(7);
if (tmp == NULL) {
    return NULL;
}
Py_DECREF(tmp);
```

Parent: [1. Extending Python with C or C++](../index.md)
