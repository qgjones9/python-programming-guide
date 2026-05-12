# [5.2. Differences Between Unix and Windows](https://docs.python.org/3/extending/windows.html#differences-between-unix-and-windows)

Local notes on **5.2. Differences Between Unix and Windows** within [*5. Building C and C++ Extensions on Windows*](https://docs.python.org/3/extending/windows.html).

- Detailed rules: **[5.2. Differences Between Unix and Windows](https://docs.python.org/3/extending/windows.html#differences-between-unix-and-windows)**.
- Companion reference: *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Returned PyObject pointers are usually new refs—pair Py_DECREF once done. */
PyObject *tmp = PyLong_FromLong(7);
if (tmp == NULL) {
    return NULL;
}
Py_DECREF(tmp);
```

Parent: [5. Building C and C++ Extensions on Windows](../index.md)
