# [Creating extensions without third party tools](https://docs.python.org/3/extending/index.html#creating-extensions-without-third-party-tools)

Section from **[Extending & Embedding — Creating extensions without third party tools](https://docs.python.org/3/extending/index.html#creating-extensions-without-third-party-tools)** (book index page). Narrative prose stays on docs.python.org.

- Canonical: [Creating extensions without third party tools](https://docs.python.org/3/extending/index.html#creating-extensions-without-third-party-tools)
- This heading is prose on `extending/index.html`; the procedural chapters collected below form the toolchain chapter list.

- **See also**: [PEP 489 – Multi-phase extension module initialization](https://peps.python.org/pep-0489/).

## Chapters under this banner

- [1. Extending Python with C or C++](extending-python-with-c-or-c/index.md)
- [2. Defining Extension Types: Tutorial](defining-extension-types-tutorial/index.md)
- [3. Defining Extension Types: Assorted Topics](defining-extension-types-assorted-topics/index.md)
- [4. Building C and C++ Extensions](building-c-and-c-extensions/index.md)
- [5. Building C and C++ Extensions on Windows](building-c-and-c-extensions-on-windows/index.md)

```c
#include <Python.h>

/* Returned PyObject pointers are usually new refs—pair Py_DECREF once done. */
PyObject *tmp = PyLong_FromLong(7);
if (tmp == NULL) {
    return NULL;
}
Py_DECREF(tmp);
```
