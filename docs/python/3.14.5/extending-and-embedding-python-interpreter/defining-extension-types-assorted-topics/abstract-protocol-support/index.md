# [3.5. Abstract Protocol Support](https://docs.python.org/3/extending/newtypes.html#abstract-protocol-support)

Local notes on **3.5. Abstract Protocol Support** within [*3. Defining Extension Types: Assorted Topics*](https://docs.python.org/3/extending/newtypes.html).

- Detailed rules: **[3.5. Abstract Protocol Support](https://docs.python.org/3/extending/newtypes.html#abstract-protocol-support)**.
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

Parent: [3. Defining Extension Types: Assorted Topics](../index.md)
