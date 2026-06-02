# [3. Defining Extension Types: Assorted Topics](https://docs.python.org/3/extending/newtypes.html)

Scratch notes backing [**3. Defining Extension Types: Assorted Topics**](https://docs.python.org/3/extending/newtypes.html) inside *[Extending and Embedding](https://docs.python.org/3/extending/index.html#extending-index)*.

### [3.1. Finalization and De-allocation](https://docs.python.org/3/extending/newtypes.html#finalization-and-de-allocation)

- Full write-up: [3.1. Finalization and De-allocation](https://docs.python.org/3/extending/newtypes.html#finalization-and-de-allocation).
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

### [3.2. Object Presentation](https://docs.python.org/3/extending/newtypes.html#object-presentation)

- Full write-up: [3.2. Object Presentation](https://docs.python.org/3/extending/newtypes.html#object-presentation).
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

### [3.3. Attribute Management](https://docs.python.org/3/extending/newtypes.html#attribute-management)

- Full write-up: [3.3. Attribute Management](https://docs.python.org/3/extending/newtypes.html#attribute-management).
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

### [3.4. Object Comparison](https://docs.python.org/3/extending/newtypes.html#object-comparison)

- Full write-up: [3.4. Object Comparison](https://docs.python.org/3/extending/newtypes.html#object-comparison).
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

### [3.5. Abstract Protocol Support](https://docs.python.org/3/extending/newtypes.html#abstract-protocol-support)

- Full write-up: [3.5. Abstract Protocol Support](https://docs.python.org/3/extending/newtypes.html#abstract-protocol-support).
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

### [3.6. Weak Reference Support](https://docs.python.org/3/extending/newtypes.html#weak-reference-support)

- Full write-up: [3.6. Weak Reference Support](https://docs.python.org/3/extending/newtypes.html#weak-reference-support).
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

### [3.7. More Suggestions](https://docs.python.org/3/extending/newtypes.html#more-suggestions)

- Full write-up: [3.7. More Suggestions](https://docs.python.org/3/extending/newtypes.html#more-suggestions).
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

- [3.1. Finalization and De-allocation](finalization-and-de-allocation/index.md)
- [3.2. Object Presentation](object-presentation/index.md)
- [3.3. Attribute Management](attribute-management/index.md)
- [3.4. Object Comparison](object-comparison/index.md)
- [3.5. Abstract Protocol Support](abstract-protocol-support/index.md)
- [3.6. Weak Reference Support](weak-reference-support/index.md)
- [3.7. More Suggestions](more-suggestions/index.md)
