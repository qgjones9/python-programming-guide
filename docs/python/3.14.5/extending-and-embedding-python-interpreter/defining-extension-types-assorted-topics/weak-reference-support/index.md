# [3.6. Weak Reference Support](https://docs.python.org/3/extending/newtypes.html#weak-reference-support)

Local notes on **3.6. Weak Reference Support** within [*3. Defining Extension Types: Assorted Topics*](https://docs.python.org/3/extending/newtypes.html).

- Detailed rules: **[3.6. Weak Reference Support](https://docs.python.org/3/extending/newtypes.html#weak-reference-support)**.
- Companion reference: *[Python/C API Reference](../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

Parent: [3. Defining Extension Types: Assorted Topics](../index.md)
