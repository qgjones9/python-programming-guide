# [Operating system thread APIs](https://docs.python.org/3/c-api/threads.html#operating-system-thread-apis)

Single-page chapter in [**Operating system thread APIs**](https://docs.python.org/3/c-api/threads.html#operating-system-thread-apis); no subdivisions below in this mirror.
Skim overview bullets here, follow the canonical link for the full narrative and API listings.

- Canonical: [Operating system thread APIs](https://docs.python.org/3/c-api/threads.html#operating-system-thread-apis)
- Treat return codes and refcount contracts exactly as documented; many helpers set the error indicator instead of asserting.
- Threading nuances (where applicable) belong to this chapter and may depend on `_Py` internals for debug builds.

```c
#include <Python.h>

// When holding the GIL, most object APIs expect the main interpreter state;
// embedding code must bracket calls appropriately (see official section on threads).
PyGILState_STATE gstate = PyGILState_Ensure();
(void)PyRun_SimpleStringFlags("pass\n", NULL);
PyGILState_Release(gstate);
```
