# [5.3. Using DLLs in Practice](https://docs.python.org/3/extending/windows.html#using-dlls-in-practice)

Local notes on **5.3. Using DLLs in Practice** within [*5. Building C and C++ Extensions on Windows*](https://docs.python.org/3/extending/windows.html).

- Detailed rules: **[5.3. Using DLLs in Practice](https://docs.python.org/3/extending/windows.html#using-dlls-in-practice)**.
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

Parent: [5. Building C and C++ Extensions on Windows](../index.md)
