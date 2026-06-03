# [loader](https://docs.python.org/3.14/glossary.html#term-loader)

An object that loads a module. It must define the `exec_module()` and `create_module()` methods to implement the [Loader](https://docs.python.org/3.14/library/importlib.html#importlib.abc.Loader) interface. A loader is typically returned by a [finder](../finder/index.md). See also:

| Reference |
|-----------|
| [Finders and loaders](https://docs.python.org/3.14/reference/import.html#finders-and-loaders) |
| [importlib.abc.Loader](https://docs.python.org/3.14/library/importlib.html#importlib.abc.Loader) |
| [PEP 302](https://peps.python.org/pep-0302/) |
