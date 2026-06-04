# [5.8. Special considerations for __main__](https://docs.python.org/3/reference/import.html#special-considerations-for-main)

The [`__main__`](https://docs.python.org/3/library/__main__.html) module is initialized at interpreter startup like [`sys`](https://docs.python.org/3/library/sys.html) and [`builtins`](https://docs.python.org/3/library/builtins.html), but it is **not** a built-in module—how it is populated depends on invocation flags (`-m`, script path, `-c`, interactive REPL, stdin).

| How Python starts | `__main__.__spec__` | Same object as `import` of that module? |
|-------------------|---------------------|----------------------------------------|
| `python -m pkg.mod` | Set to that module's spec | **No** — distinct module objects |
| Directory/zip `sys.path` entry execution | Set appropriately | Context-dependent |
| `python script.py` / interactive / `-c` | **`None`** | N/A |

Even when `-m` loads an importable module, `__main__` and the imported module remain **distinct**: code under `if __name__ == "__main__":` runs only when that file populates the main namespace, not during a normal import of the same file.

```python
# Goal: __main__ always reports __name__ == "__main__" in this process
import __main__

assert __main__.__name__ == "__main__"
assert hasattr(__main__, "__dict__")
```

```python
# Goal: __spec__ is None when the interpreter was not started with -m
import __main__

# Subagent / script entry: typically no module spec for __main__
assert __main__.__spec__ is None or __main__.__spec__.name.endswith("__main__")
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Expecting `import myapp` to run `if __name__ == "__main__"` block | Guard runs only under `-m` or direct execution | Expose a `main()` and call it explicitly |
| Assuming `__main__.__spec__` is always set | Direct script execution leaves it `None` | Use `python -m pkg` when metadata is required |
| Treating `__main__` as alias of the source module under `-m` | Two module objects; singletons diverge | Store shared state on imported modules, not only `__main__` |

Parent: [5. The import system](../index.md)
