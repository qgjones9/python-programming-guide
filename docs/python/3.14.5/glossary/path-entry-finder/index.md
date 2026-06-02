# [path entry finder](https://docs.python.org/3.14/glossary.html#term-path-entry-finder)

A [finder](../finder/index.md) returned by a callable on [sys.path_hooks](https://docs.python.org/3.14/library/sys.html#sys.path_hooks)
(i.e. a [path entry hook](../path-entry-hook/index.md)) which knows how to locate modules given
a [path entry](../path-entry/index.md).

See [importlib.abc.PathEntryFinder](https://docs.python.org/3.14/library/importlib.html#importlib.abc.PathEntryFinder) for the methods that path entry
finders implement.
