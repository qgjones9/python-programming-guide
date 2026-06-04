# [5. The import system](https://docs.python.org/3/reference/import.html)

The import system is how Python code in one module gains access to code in another. An `import` statement combines **search** (locate the module) and **binding** (attach it to a name in the local namespace). Since Python 3.3, the full machinery is exposed through [`sys.meta_path`](https://docs.python.org/3/library/sys.html#sys.meta_path) and related hooks—there is no hidden legacy path. Normative wording lives on [docs.python.org](https://docs.python.org/3/reference/import.html); these notes distill the chapter for quick study.

| Phase | What happens | Key objects |
|-------|--------------|-------------|
| Cache lookup | Return an already-loaded module if present | `sys.modules` |
| Meta-path search | Finders locate a module and return a spec | `sys.meta_path`, `ModuleSpec` |
| Loading | Loader executes module code into a namespace | `Loader.exec_module()` |
| Binding | `import` binds names in the importer's scope | `import` / `from … import` |

```python
# Goal: import is search + bind; second import reuses the cached module object
import sys
import json

first_id = id(json)
import json as alias
assert id(alias) == first_id
assert sys.modules["json"] is json
```

## Sections in this repo

| Section | Summary |
|---------|---------|
| [5.1. importlib](importlib/index.md) | Programmatic import API layered on the same machinery |
| [5.2. Packages](packages/index.md) | Regular vs namespace packages; `__path__` marks packages |
| [5.3. Searching](searching/index.md) | `sys.modules`, finders, loaders, meta path, hooks |
| [5.4. Loading](loading/index.md) | `exec_module`, specs, submodules, bytecode caches |
| [5.5. The Path Based Finder](the-path-based-finder/index.md) | `sys.path`, path hooks, path entry finders |
| [5.6. Replacing the standard import system](replacing-the-standard-import-system/index.md) | Custom meta path hooks and `__import__` overrides |
| [5.7. Package Relative Imports](package-relative-imports/index.md) | Leading-dot syntax and parent traversal |
| [5.8. Special considerations for __main__](special-considerations-for-main/index.md) | How `__main__` is initialized and when `__spec__` is set |
| [5.9. References](references/index.md) | PEP history for the modern import protocol |
