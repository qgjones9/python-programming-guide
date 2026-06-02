# [Embedding the CPython runtime in a larger application](https://docs.python.org/3/extending/index.html#embedding-the-cpython-runtime-in-a-larger-application)

Section from **[Extending & Embedding — Embedding the CPython runtime in a larger application](https://docs.python.org/3/extending/index.html#embedding-the-cpython-runtime-in-a-larger-application)** (book index page). Narrative prose stays on docs.python.org.

- Canonical: [Embedding the CPython runtime in a larger application](https://docs.python.org/3/extending/index.html#embedding-the-cpython-runtime-in-a-larger-application)
- Embedding calls `Py_Initialize` / teardown sequences; pitfalls differ from extension modules shipped as `.so`/`.pyd`.

- Follow **[1. Embedding Python in Another Application](embedding-python-in-another-application/index.md)** for the runnable walkthrough.

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
