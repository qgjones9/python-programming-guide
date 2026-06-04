# [__main__ — Top-level code environment](https://docs.python.org/3/library/__main__.html)

[`__main__`](https://docs.python.org/3/library/__main__.html) is both a **module name** and a runtime concept: the namespace where **top-level script code** executes. Whether `__name__ == "__main__"` distinguishes direct execution from import. Packages expose `python -m pkg` via `pkg/__main__.py`. Reference: [docs.python.org](https://docs.python.org/3/library/__main__.html).

---

## Top-level code environment — [What is the "top-level code environment"?](https://docs.python.org/3/library/__main__.html#what-is-the-top-level-code-environment)

| Invocation | `__name__` | `__main__` module |
|------------|------------|-------------------|
| `python script.py` | `"__main__"` | Script's globals dict |
| `python -m pkg.mod` | `"__main__"` in that module | Module's namespace |
| `import pkg.mod` | `"pkg.mod"` | Separate import loader state |

The `__main__` **module object** (`sys.modules["__main__"]`) always refers to the initial script entry, even after imports.

---

## Idiomatic usage — [Idiomatic Usage](https://docs.python.org/3/library/__main__.html#idiomatic-usage)

```python
# Goal: gate CLI behavior on direct execution
def main():
    return "ran"

if __name__ == "__main__":
    result = main()
    assert result == "ran"
else:
    # Imported as a library — skip CLI side effects
    pass
```

Place side effects (argument parsing, `main()`) behind the guard; keep importable API at module level.

---

## Packaging — [__main__.py in Python Packages](https://docs.python.org/3/library/__main__.html#main-py-in-python-packages)

A package directory may include `__main__.py` so `python -m mypkg` runs package-level CLI code. [`zipapp`](../../software-packaging-and-distribution/zipapp-manage-executable-python-zip-archives/index.md) archives require a root `__main__.py` for execution.

---

## Best practices

| Practice | Why |
|----------|-----|
| Keep **`main()` pure enough to test** | Import path stays unit-testable |
| Use **`python -m pip`** style for CLIs | Ensures package context and `sys.path[0]` |
| Document **`python -m pkg`** entry in README | Users discover console scripts |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Heavy work at import time | Slow `import pkg` | Guard with `if __name__ == "__main__"` |
| Two modules both named `__main__` confusion | Only one `sys.modules["__main__"]` | Remember it tracks the entry script |

---

## See also

- [`runpy`](https://docs.python.org/3/library/runpy.html) — programmatic `-m` execution
- [`zipapp`](../../software-packaging-and-distribution/zipapp-manage-executable-python-zip-archives/index.md) — zip application entry points
