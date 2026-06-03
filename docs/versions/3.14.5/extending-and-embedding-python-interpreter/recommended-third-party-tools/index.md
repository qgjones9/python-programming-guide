# [Recommended third party tools](https://docs.python.org/3/extending/index.html#recommended-third-party-tools)

Section from **[Extending & Embedding — Recommended third party tools](https://docs.python.org/3/extending/index.html#recommended-third-party-tools)** (book index page). Narrative prose stays on docs.python.org.

- Canonical: [Recommended third party tools](https://docs.python.org/3/extending/index.html#recommended-third-party-tools)
- Prefer maintained bindgens (PyO3/pybind11/Cython, etc.) linked from the upstream guide before handwriting everything in raw C.
- Dive into *[Python/C API](https://docs.python.org/3/c-api/index.html)* when you bypass higher-level scaffolding.

## See also

- [Creating extensions without third party tools](../creating-extensions-without-third-party-tools/index.md)

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```
