# [Python Runtime Services](https://docs.python.org/3/library/python.html)

**Python Runtime Services** modules sit closest to the interpreter: introspection, startup hooks, warnings, garbage collection, and packaging-related runtime glue. They expose `sys` parameters, help debuggers and profilers, and shape how code runs at import time and shutdown. Full reference: [docs.python.org](https://docs.python.org/3/library/python.html).

See also [`concurrent.interpreters`](../custom-python-interpreters/concurrent-interpreters/index.md) for subinterpreter APIs that similarly expose core runtime behavior.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`sys`](sys-system-specific-parameters-and-functions/index.md) | Interpreter parameters, streams, path, exit, audit hooks |
| [`sys.monitoring`](sysmonitoring-execution-event-monitoring/index.md) | Low-overhead execution event callbacks (3.12+) |
| [`sysconfig`](sysconfig-provide-access-to-pythons-configuration-information/index.md) | Build-time installation paths and Makefile variables |
| [`builtins`](builtins-built-in-objects/index.md) | Namespace of built-in names (`len`, `open`, …) |
| [`__main__`](__main__-top-level-code-environment/index.md) | Top-level script vs import semantics |
| [`warnings`](warnings-warning-control/index.md) | Filter and emit warning categories |
| [`dataclasses`](dataclasses-data-classes/index.md) | `@dataclass` boilerplate reduction |
| [`contextlib`](contextlib-utilities-for-with-statement-contexts/index.md) | Context manager helpers and decorators |
| [`abc`](abc-abstract-base-classes/index.md) | Abstract base classes and `@abstractmethod` |
| [`atexit`](atexit-exit-handlers/index.md) | Register functions for interpreter shutdown |
| [`traceback`](traceback-print-or-retrieve-a-stack-traceback/index.md) | Format and print exception tracebacks |
| [`__future__`](__future__-future-statement-definitions/index.md) | Opt-in language semantics via `from __future__ import …` |
| [`gc`](gc-garbage-collector-interface/index.md) | Cycle collector controls and statistics |
| [`inspect`](inspect-inspect-live-objects/index.md) | Introspect live objects, frames, signatures |
| [`annotationlib`](annotationlib-functionality-for-introspecting-annotations/index.md) | Reliable annotation retrieval (3.14+, PEP 649/749) |
| [`site`](site-site-specific-configuration-hook/index.md) | Site-packages path setup at startup |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Read Python version, argv, path | [`sys`](sys-system-specific-parameters-and-functions/index.md) |
| Debugger / coverage / profiler hooks | [`sys.monitoring`](sysmonitoring-execution-event-monitoring/index.md) |
| Find `include` or `stdlib` paths for builds | [`sysconfig`](sysconfig-provide-access-to-pythons-configuration-information/index.md) |
| Control deprecation noise | [`warnings`](warnings-warning-control/index.md) |
| Structured data containers | [`dataclasses`](dataclasses-data-classes/index.md) |
| Resource cleanup patterns | [`contextlib`](contextlib-utilities-for-with-statement-contexts/index.md) |
| Plugin interfaces with enforced methods | [`abc`](abc-abstract-base-classes/index.md) |
| Flush logs on normal exit | [`atexit`](atexit-exit-handlers/index.md) |
| Pretty-print errors in apps | [`traceback`](traceback-print-or-retrieve-a-stack-traceback/index.md) |
| Postpone annotation evaluation | [`__future__`](__future__-future-statement-definitions/index.md) or 3.14 deferred defaults |
| Debug reference cycles | [`gc`](gc-garbage-collector-interface/index.md) |
| Framework reflection | [`inspect`](inspect-inspect-live-objects/index.md) + [`annotationlib`](annotationlib-functionality-for-introspecting-annotations/index.md) |
| Customize import path at startup | [`site`](site-site-specific-configuration-hook/index.md) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Prefer **`warnings` filters** over silencing stderr | Keeps signal while reducing noise |
| Use **`contextlib.closing`** / **`suppress`** for clarity | Replaces ad-hoc try/finally |
| Register **`atexit`** for best-effort cleanup only | Not called on hard kill or `os._exit` |
| Introspect with **`inspect.signature`** before calling unknown callables | Safer plugin loading |
| Read annotations via **`annotationlib.get_annotations`** on 3.14+ | Handles forward refs and deferred evaluation |

```python
# Goal: runtime trio — sys identity, warning capture, dataclass instance
import sys
import warnings
from dataclasses import dataclass

assert sys.version_info.major == 3
with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    warnings.warn("demo", UserWarning)
    assert len(log) == 1

@dataclass
class Point:
    x: int
    y: int

p = Point(1, 2)
assert p.x + p.y == 3
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [sys — System-specific parameters and functions](sys-system-specific-parameters-and-functions/index.md) | Version, path, hooks, recursion limits |
| [sys.monitoring — Execution event monitoring](sysmonitoring-execution-event-monitoring/index.md) | Tool IDs, event sets, callbacks |
| [sysconfig — Provide access to Python's configuration information](sysconfig-provide-access-to-pythons-configuration-information/index.md) | Install schemes and config vars |
| [builtins — Built-in objects](builtins-built-in-objects/index.md) | Built-in namespace module |
| [__main__ — Top-level code environment](__main__-top-level-code-environment/index.md) | Script entry points and `-m` |
| [warnings — Warning control](warnings-warning-control/index.md) | Filters, categories, simplefilter |
| [dataclasses — Data Classes](dataclasses-data-classes/index.md) | Field generation, frozen, slots |
| [contextlib — Utilities for with-statement contexts](contextlib-utilities-for-with-statement-contexts/index.md) | `@contextmanager`, ExitStack |
| [abc — Abstract Base Classes](abc-abstract-base-classes/index.md) | ABCMeta, virtual subclasses |
| [atexit — Exit handlers](atexit-exit-handlers/index.md) | LIFO shutdown callbacks |
| [traceback — Print or retrieve a stack traceback](traceback-print-or-retrieve-a-stack-traceback/index.md) | Stack formatting utilities |
| [__future__ — Future statement definitions](__future__-future-statement-definitions/index.md) | Feature flags for syntax semantics |
| [gc — Garbage Collector interface](gc-garbage-collector-interface/index.md) | Collection, thresholds, debug |
| [inspect — Inspect live objects](inspect-inspect-live-objects/index.md) | Signatures, source, stack frames |
| [annotationlib — Functionality for introspecting annotations](annotationlib-functionality-for-introspecting-annotations/index.md) | `get_annotations`, `Format` enum |
| [site — Site-specific configuration hook](site-site-specific-configuration-hook/index.md) | site-packages discovery |
