# [3.2. Object Presentation](https://docs.python.org/3/extending/newtypes.html#object-presentation)

Local notes on **3.2. Object Presentation** within [*3. Defining Extension Types: Assorted Topics*](https://docs.python.org/3/extending/newtypes.html).

- Detailed rules: **[3.2. Object Presentation](https://docs.python.org/3/extending/newtypes.html#object-presentation)**.
- Companion reference: *[Python/C API Reference](../../../python-c-api-reference-manual/index.md)* for every `Py*` symbol you call.

```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```

Parent: [3. Defining Extension Types: Assorted Topics](../index.md)
