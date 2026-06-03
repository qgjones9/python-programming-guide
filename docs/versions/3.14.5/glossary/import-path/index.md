# [import path](https://docs.python.org/3.14/glossary.html#term-import-path)

A list of locations (or [path entries](../path-entry/index.md)) that are
searched by the [path based finder](../path-based-finder/index.md) for modules to import. During
import, this list of locations usually comes from [sys.path](https://docs.python.org/3.14/library/sys.html#sys.path), but
for subpackages it may also come from the parent package’s `__path__`
attribute.
