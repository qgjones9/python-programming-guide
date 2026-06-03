# [namespace package](https://docs.python.org/3.14/glossary.html#term-namespace-package)

A [package](../package/index.md) which serves only as a container for subpackages. Namespace packages may have no physical representation, and specifically are not like a [regular package](../regular-package/index.md) because they have no `__init__.py` file.

Namespace packages allow several individually installable packages to have a common parent package. Otherwise, it is recommended to use a [regular package](../regular-package/index.md).

For more information, see [PEP 420](https://peps.python.org/pep-0420/) and [Namespace packages](https://docs.python.org/3.14/reference/import.html#reference-namespace-package).

See also [module](../module/index.md).
