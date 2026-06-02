# [2.1. The Basics](https://docs.python.org/3/extending/newtypes_tutorial.html#the-basics)

Local notes on **2.1. The Basics** within [*2. Defining Extension Types: Tutorial*](https://docs.python.org/3/extending/newtypes_tutorial.html).

- Detailed rules: **[2.1. The Basics](https://docs.python.org/3/extending/newtypes_tutorial.html#the-basics)**.
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

Parent: [2. Defining Extension Types: Tutorial](../index.md)
