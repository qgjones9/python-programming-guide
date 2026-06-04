# [9.1. Complete Python programs](https://docs.python.org/3/reference/toplevel_components.html#complete-python-programs)

A **complete Python program** is the unit CPython executes when you are not in “one line at a time” interactive mode. The reference defines a **minimally initialized** environment and treats the program’s syntax as [**file input**](file-input/index.md) (statements until end of file).

---

## Startup environment

| Component | State at program start |
|-----------|-------------------------|
| Built-in and standard library modules | Present in `sys.modules`, but **not** initialized (except as noted below) |
| `sys` | Initialized (system services) |
| `builtins` | Initialized (built-in functions, exceptions, `None`) |
| `__main__` | Initialized; provides **globals/locals** for top-level execution |

Top-level assignments and `def` / `class` at module scope bind names in `__main__.__dict__` (what you see as “module globals” when `python script.py` runs).

---

## How the interpreter receives a complete program

| Delivery | Behavior |
|----------|----------|
| `python -c '…'` | String is a complete program (`file_input`) |
| `python path/to/script.py` | File is a complete program |
| `python` with stdin **not** a TTY | Stdin is read as a complete program |
| Stdin or script path **is** a TTY | Interpreter enters **interactive** mode (see [9.3](../interactive-input/index.md)) |

Interactive mode uses the same initial environment but executes **one** statement per prompt instead of reading until `ENDMARKER` for the whole file.

```python
# Goal: __main__ namespace holds script-level globals
import __main__

__main__.program_id = 9
assert __main__.program_id == 9
```

```python
# Goal: -c and file execution both use file_input (statements, not a lone expression)
# Simulate a one-statement "program" body:
body = "result = len('abc')\n"
ns: dict[str, object] = {}
exec(compile(body, "<prog>", "exec"), ns, ns)
assert ns["result"] == 3
```

Parent: [9. Top-level components](../index.md)
