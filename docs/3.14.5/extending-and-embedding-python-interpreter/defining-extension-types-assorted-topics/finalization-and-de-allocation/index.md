# [3.1. Finalization and De-allocation](https://docs.python.org/3/extending/newtypes.html#finalization-and-de-allocation)

Local notes on **3.1. Finalization and De-allocation** within [*3. Defining Extension Types: Assorted Topics*](https://docs.python.org/3/extending/newtypes.html).

- Detailed rules: **[3.1. Finalization and De-allocation](https://docs.python.org/3/extending/newtypes.html#finalization-and-de-allocation)**.
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

Parent: [3. Defining Extension Types: Assorted Topics](../index.md)
