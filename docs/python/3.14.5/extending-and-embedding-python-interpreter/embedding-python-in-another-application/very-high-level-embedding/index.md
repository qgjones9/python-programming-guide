# [1.1. Very High Level Embedding](https://docs.python.org/3/extending/embedding.html#very-high-level-embedding)

Local notes on **1.1. Very High Level Embedding** within [*1. Embedding Python in Another Application*](https://docs.python.org/3/extending/embedding.html).

- Detailed rules: **[1.1. Very High Level Embedding](https://docs.python.org/3/extending/embedding.html#very-high-level-embedding)**.
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

Parent: [1. Embedding Python in Another Application](../index.md)
