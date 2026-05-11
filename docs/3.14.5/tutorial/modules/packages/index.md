# [Packages](https://docs.python.org/3/tutorial/modules.html#packages)

Condensed notes for **§6.4 — Packages** in the [Python Tutorial](https://docs.python.org/3/tutorial/modules.html): hierarchical modules, `__init__.py`, intra-package imports, and **`__all__`**. For directory layout diagrams and edge cases, follow the official page.

### Why packages exist

- **Packages** map dotted module names to nested directories so large libraries can split into coherent submodules (**`xml.sax.handler`**, **`collections.abc`**, …).
- **`import sound.effects.echo`** loads **`sound`**, then **`sound.effects`**, then **`sound.effects.echo`**; each segment must be importable as a module or package.

```python
# The standard library itself ships as packages; importing a submodule does not flatten names.
import urllib.parse

# quote() leaves "/" unescaped unless you clear `safe` — match real default behavior.
assert urllib.parse.quote("a/b") == "a/b"
assert urllib.parse.quote("a b") == "a%20b"
```

### Controlling `from package import *`

- A package’s **`__init__.py`** may define **`__all__`** to list names exported by **`from package import *`**; without **`__all__`**, the behavior is less predictable for subpackages.

```python
# __all__ on a module controls star-import when defined.
__all__ = ("public",)


def public() -> str:
    return "yes"


def _private() -> str:
    return "no"


assert public() == "yes"
```

## Sections in this repo

- [Importing from a Package](importing-from-a-package/index.md)
- [Intra-package References](intra-package-references/index.md)
- [Packages in Multiple Directories](packages-in-multiple-directories/index.md)

Parent: [Modules](../index.md)
