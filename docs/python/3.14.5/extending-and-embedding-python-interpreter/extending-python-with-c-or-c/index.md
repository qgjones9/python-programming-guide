# [1. Extending Python with C or C++](https://docs.python.org/3/extending/extending.html)

Scratch notes backing [**1. Extending Python with C or C++**](https://docs.python.org/3/extending/extending.html) inside *[Extending and Embedding](https://docs.python.org/3/extending/index.html#extending-index)*.

### [1.1. A Simple Example](https://docs.python.org/3/extending/extending.html#a-simple-example)

- Full write-up: [1.1. A Simple Example](https://docs.python.org/3/extending/extending.html#a-simple-example).
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

### [1.2. Intermezzo: Errors and Exceptions](https://docs.python.org/3/extending/extending.html#intermezzo-errors-and-exceptions)

- Full write-up: [1.2. Intermezzo: Errors and Exceptions](https://docs.python.org/3/extending/extending.html#intermezzo-errors-and-exceptions).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [1.3. Back to the Example](https://docs.python.org/3/extending/extending.html#back-to-the-example)

- Full write-up: [1.3. Back to the Example](https://docs.python.org/3/extending/extending.html#back-to-the-example).
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

### [1.4. The Module’s Method Table and Initialization Function](https://docs.python.org/3/extending/extending.html#the-module-s-method-table-and-initialization-function)

- Full write-up: [1.4. The Module’s Method Table and Initialization Function](https://docs.python.org/3/extending/extending.html#the-module-s-method-table-and-initialization-function).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [1.5. Compilation and Linkage](https://docs.python.org/3/extending/extending.html#compilation-and-linkage)

- Full write-up: [1.5. Compilation and Linkage](https://docs.python.org/3/extending/extending.html#compilation-and-linkage).
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

### [1.6. Calling Python Functions from C](https://docs.python.org/3/extending/extending.html#calling-python-functions-from-c)

- Full write-up: [1.6. Calling Python Functions from C](https://docs.python.org/3/extending/extending.html#calling-python-functions-from-c).
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

### [1.7. Extracting Parameters in Extension Functions](https://docs.python.org/3/extending/extending.html#extracting-parameters-in-extension-functions)

- Full write-up: [1.7. Extracting Parameters in Extension Functions](https://docs.python.org/3/extending/extending.html#extracting-parameters-in-extension-functions).
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

### [1.8. Keyword Parameters for Extension Functions](https://docs.python.org/3/extending/extending.html#keyword-parameters-for-extension-functions)

- Full write-up: [1.8. Keyword Parameters for Extension Functions](https://docs.python.org/3/extending/extending.html#keyword-parameters-for-extension-functions).
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

### [1.9. Building Arbitrary Values](https://docs.python.org/3/extending/extending.html#building-arbitrary-values)

- Full write-up: [1.9. Building Arbitrary Values](https://docs.python.org/3/extending/extending.html#building-arbitrary-values).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [1.10. Reference Counts](https://docs.python.org/3/extending/extending.html#reference-counts)

- Full write-up: [1.10. Reference Counts](https://docs.python.org/3/extending/extending.html#reference-counts).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [1.11. Writing Extensions in C++](https://docs.python.org/3/extending/extending.html#writing-extensions-in-c)

- Full write-up: [1.11. Writing Extensions in C++](https://docs.python.org/3/extending/extending.html#writing-extensions-in-c).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [1.12. Providing a C API for an Extension Module](https://docs.python.org/3/extending/extending.html#providing-a-c-api-for-an-extension-module)

- Full write-up: [1.12. Providing a C API for an Extension Module](https://docs.python.org/3/extending/extending.html#providing-a-c-api-for-an-extension-module).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

## Sections in this repo

- [1.1. A Simple Example](a-simple-example/index.md)
- [1.2. Intermezzo: Errors and Exceptions](intermezzo-errors-and-exceptions/index.md)
- [1.3. Back to the Example](back-to-the-example/index.md)
- [1.4. The Module’s Method Table and Initialization Function](the-module-s-method-table-and-initialization-function/index.md)
- [1.5. Compilation and Linkage](compilation-and-linkage/index.md)
- [1.6. Calling Python Functions from C](calling-python-functions-from-c/index.md)
- [1.7. Extracting Parameters in Extension Functions](extracting-parameters-in-extension-functions/index.md)
- [1.8. Keyword Parameters for Extension Functions](keyword-parameters-for-extension-functions/index.md)
- [1.9. Building Arbitrary Values](building-arbitrary-values/index.md)
- [1.10. Reference Counts](reference-counts/index.md)
- [1.11. Writing Extensions in C++](writing-extensions-in-c/index.md)
- [1.12. Providing a C API for an Extension Module](providing-a-c-api-for-an-extension-module/index.md)
