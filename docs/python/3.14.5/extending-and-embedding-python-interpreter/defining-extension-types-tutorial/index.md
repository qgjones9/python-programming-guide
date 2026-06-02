# [2. Defining Extension Types: Tutorial](https://docs.python.org/3/extending/newtypes_tutorial.html)

Scratch notes backing [**2. Defining Extension Types: Tutorial**](https://docs.python.org/3/extending/newtypes_tutorial.html) inside *[Extending and Embedding](https://docs.python.org/3/extending/index.html#extending-index)*.

### [2.1. The Basics](https://docs.python.org/3/extending/newtypes_tutorial.html#the-basics)

- Full write-up: [2.1. The Basics](https://docs.python.org/3/extending/newtypes_tutorial.html#the-basics).
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

### [2.2. Adding data and methods to the Basic example](https://docs.python.org/3/extending/newtypes_tutorial.html#adding-data-and-methods-to-the-basic-example)

- Full write-up: [2.2. Adding data and methods to the Basic example](https://docs.python.org/3/extending/newtypes_tutorial.html#adding-data-and-methods-to-the-basic-example).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [2.3. Providing finer control over data attributes](https://docs.python.org/3/extending/newtypes_tutorial.html#providing-finer-control-over-data-attributes)

- Full write-up: [2.3. Providing finer control over data attributes](https://docs.python.org/3/extending/newtypes_tutorial.html#providing-finer-control-over-data-attributes).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

### [2.4. Supporting cyclic garbage collection](https://docs.python.org/3/extending/newtypes_tutorial.html#supporting-cyclic-garbage-collection)

- Full write-up: [2.4. Supporting cyclic garbage collection](https://docs.python.org/3/extending/newtypes_tutorial.html#supporting-cyclic-garbage-collection).
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

### [2.5. Subclassing other types](https://docs.python.org/3/extending/newtypes_tutorial.html#subclassing-other-types)

- Full write-up: [2.5. Subclassing other types](https://docs.python.org/3/extending/newtypes_tutorial.html#subclassing-other-types).
- Cross-check refcount / error conventions with the *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* mirror when coding against `Python.h`.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

## Sections in this repo

- [2.1. The Basics](the-basics/index.md)
- [2.2. Adding data and methods to the Basic example](adding-data-and-methods-to-the-basic-example/index.md)
- [2.3. Providing finer control over data attributes](providing-finer-control-over-data-attributes/index.md)
- [2.4. Supporting cyclic garbage collection](supporting-cyclic-garbage-collection/index.md)
- [2.5. Subclassing other types](subclassing-other-types/index.md)
