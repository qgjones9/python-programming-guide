# [finder](https://docs.python.org/3.14/glossary.html#term-finder)

An object that tries to find the [loader](../loader/index.md) for a module that is being imported.

There are two types of finder: [meta path finders](../meta-path-finder/index.md) for use with [sys.meta_path](https://docs.python.org/3.14/library/sys.html#sys.meta_path), and [path entry finders](../path-entry-finder/index.md) for use with [sys.path_hooks](https://docs.python.org/3.14/library/sys.html#sys.path_hooks).

See [Finders and loaders](https://docs.python.org/3.14/reference/import.html#finders-and-loaders) and [importlib](https://docs.python.org/3.14/library/importlib.html#module-importlib) for much more detail.
