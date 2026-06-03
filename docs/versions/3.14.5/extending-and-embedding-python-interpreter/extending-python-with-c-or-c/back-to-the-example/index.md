# [1.3. Back to the Example](https://docs.python.org/3/extending/extending.html#back-to-the-example)

Local notes on **1.3. Back to the Example** within [*1. Extending Python with C or C++*](https://docs.python.org/3/extending/extending.html).

- Detailed rules: **[1.3. Back to the Example](https://docs.python.org/3/extending/extending.html#back-to-the-example)**.
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
