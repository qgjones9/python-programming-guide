# [Generating Execution Events](https://docs.python.org/3/c-api/monitoring.html#generating-execution-events)

Local notes aligned with [**Generating Execution Events**](https://docs.python.org/3/c-api/monitoring.html#generating-execution-events) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Managing the Monitoring State](https://docs.python.org/3/c-api/monitoring.html#managing-the-monitoring-state)

- Official docs: [Managing the Monitoring State](https://docs.python.org/3/c-api/monitoring.html#managing-the-monitoring-state) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

// When holding the GIL, most object APIs expect the main interpreter state;
// embedding code must bracket calls appropriately (see official section on threads).
PyGILState_STATE gstate = PyGILState_Ensure();
(void)PyRun_SimpleStringFlags("pass\n", NULL);
PyGILState_Release(gstate);
```

## Sections in this repo

- [Managing the Monitoring State](managing-the-monitoring-state/index.md)
