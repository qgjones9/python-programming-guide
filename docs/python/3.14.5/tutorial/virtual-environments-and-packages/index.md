# [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)

Condensed notes for [chapter 12 — Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html): isolating dependencies with **`venv`**, activating environments, and installing packages with **`pip`**.

```python
import sys

# Virtual environments point `sys.prefix` at the env directory instead of the global install.
assert isinstance(sys.prefix, str) and len(sys.prefix) > 0
```

### 12.1 — [Introduction](https://docs.python.org/3/tutorial/venv.html#introduction)

- A **venv** is a lightweight directory tree containing its own **`python`** and **`site-packages`**, so projects do not fight over library versions.

### 12.2 — [Creating Virtual Environments](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)

```python
import venv

# `EnvBuilder` is the programmatic API behind `python -m venv .venv`.
builder = venv.EnvBuilder(with_pip=True)
assert callable(builder.create)
```

### 12.3 — [Managing Packages with pip](https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip)

```python
import importlib.util

# `find_spec` is the supported way to test whether an optional dependency is importable.
spec = importlib.util.find_spec("pip")
assert spec is None or spec.name == "pip"
```

## Sections in this repo

- [Introduction](introduction/index.md)
- [Creating Virtual Environments](creating-virtual-environments/index.md)
- [Managing Packages with pip](managing-packages-with-pip/index.md)

Next: [Interactive Input Editing and History Substitution](../interactive-input-editing-and-history-substitution/index.md)
