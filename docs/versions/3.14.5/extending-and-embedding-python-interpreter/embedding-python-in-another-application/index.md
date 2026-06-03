# [1. Embedding Python in Another Application](https://docs.python.org/3/extending/embedding.html)

Scratch notes backing [**1. Embedding Python in Another Application**](https://docs.python.org/3/extending/embedding.html) inside *[Extending and Embedding](https://docs.python.org/3/extending/index.html#extending-index)*.

### [1.1. Very High Level Embedding](https://docs.python.org/3/extending/embedding.html#very-high-level-embedding)

- Full write-up: [1.1. Very High Level Embedding](https://docs.python.org/3/extending/embedding.html#very-high-level-embedding).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [1.2. Beyond Very High Level Embedding: An overview](https://docs.python.org/3/extending/embedding.html#beyond-very-high-level-embedding-an-overview)

- Full write-up: [1.2. Beyond Very High Level Embedding: An overview](https://docs.python.org/3/extending/embedding.html#beyond-very-high-level-embedding-an-overview).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Returned PyObject pointers are usually new refs—pair Py_DECREF once done. */
PyObject *tmp = PyLong_FromLong(7);
if (tmp == NULL) {
    return NULL;
}
Py_DECREF(tmp);
```

### [1.3. Pure Embedding](https://docs.python.org/3/extending/embedding.html#pure-embedding)

- Full write-up: [1.3. Pure Embedding](https://docs.python.org/3/extending/embedding.html#pure-embedding).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Returned PyObject pointers are usually new refs—pair Py_DECREF once done. */
PyObject *tmp = PyLong_FromLong(7);
if (tmp == NULL) {
    return NULL;
}
Py_DECREF(tmp);
```

### [1.4. Extending Embedded Python](https://docs.python.org/3/extending/embedding.html#extending-embedded-python)

- Full write-up: [1.4. Extending Embedded Python](https://docs.python.org/3/extending/embedding.html#extending-embedded-python).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [1.5. Embedding Python in C++](https://docs.python.org/3/extending/embedding.html#embedding-python-in-c)

- Full write-up: [1.5. Embedding Python in C++](https://docs.python.org/3/extending/embedding.html#embedding-python-in-c).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

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

### [1.6. Compiling and Linking under Unix-like systems](https://docs.python.org/3/extending/embedding.html#compiling-and-linking-under-unix-like-systems)

- Full write-up: [1.6. Compiling and Linking under Unix-like systems](https://docs.python.org/3/extending/embedding.html#compiling-and-linking-under-unix-like-systems).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Returned PyObject pointers are usually new refs—pair Py_DECREF once done. */
PyObject *tmp = PyLong_FromLong(7);
if (tmp == NULL) {
    return NULL;
}
Py_DECREF(tmp);
```

## Sections in this repo

- [1.1. Very High Level Embedding](very-high-level-embedding/index.md)
- [1.2. Beyond Very High Level Embedding: An overview](beyond-very-high-level-embedding-an-overview/index.md)
- [1.3. Pure Embedding](pure-embedding/index.md)
- [1.4. Extending Embedded Python](extending-embedded-python/index.md)
- [1.5. Embedding Python in C++](embedding-python-in-c/index.md)
- [1.6. Compiling and Linking under Unix-like systems](compiling-and-linking-under-unix-like-systems/index.md)
