# [5. Building C and C++ Extensions on Windows](https://docs.python.org/3/extending/windows.html)

Scratch notes backing [**5. Building C and C++ Extensions on Windows**](https://docs.python.org/3/extending/windows.html) inside *[Extending and Embedding](https://docs.python.org/3/extending/index.html#extending-index)*.

### [5.1. A Cookbook Approach](https://docs.python.org/3/extending/windows.html#a-cookbook-approach)

- Full write-up: [5.1. A Cookbook Approach](https://docs.python.org/3/extending/windows.html#a-cookbook-approach).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Returned PyObject pointers are usually new refs—pair Py_DECREF once done. */
PyObject *tmp = PyLong_FromLong(7);
if (tmp == NULL) {
    return NULL;
}
Py_DECREF(tmp);
```

### [5.2. Differences Between Unix and Windows](https://docs.python.org/3/extending/windows.html#differences-between-unix-and-windows)

- Full write-up: [5.2. Differences Between Unix and Windows](https://docs.python.org/3/extending/windows.html#differences-between-unix-and-windows).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

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

### [5.3. Using DLLs in Practice](https://docs.python.org/3/extending/windows.html#using-dlls-in-practice)

- Full write-up: [5.3. Using DLLs in Practice](https://docs.python.org/3/extending/windows.html#using-dlls-in-practice).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

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

## Sections in this repo

- [5.1. A Cookbook Approach](a-cookbook-approach/index.md)
- [5.2. Differences Between Unix and Windows](differences-between-unix-and-windows/index.md)
- [5.3. Using DLLs in Practice](using-dlls-in-practice/index.md)
