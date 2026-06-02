# [1.6. Calling Python Functions from C](https://docs.python.org/3/extending/extending.html#calling-python-functions-from-c)

Local notes on **1.6. Calling Python Functions from C** within [*1. Extending Python with C or C++*](https://docs.python.org/3/extending/extending.html).

- Detailed rules: **[1.6. Calling Python Functions from C](https://docs.python.org/3/extending/extending.html#calling-python-functions-from-c)**.
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
