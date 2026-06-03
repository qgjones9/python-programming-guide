# [global interpreter lock](https://docs.python.org/3.14/glossary.html#term-global-interpreter-lock)

The mechanism used by the [CPython](../CPython/index.md) interpreter to assure that
only one thread executes Python [bytecode](../bytecode/index.md) at a time.
This simplifies the CPython implementation by making the object model
(including critical built-in types such as [dict](https://docs.python.org/3.14/library/stdtypes.html#dict)) implicitly
safe against concurrent access.  Locking the entire interpreter
makes it easier for the interpreter to be multi-threaded, at the
expense of much of the parallelism afforded by multi-processor
machines.

However, some extension modules, either standard or third-party,
are designed so as to release the GIL when doing computationally intensive
tasks such as compression or hashing.  Also, the GIL is always released
when doing I/O.

As of Python 3.13, the GIL can be disabled using the [--disable-gil](https://docs.python.org/3.14/using/configure.html#cmdoption-disable-gil)
build configuration. After building Python with this option, code must be
run with [-Xgil=0](https://docs.python.org/3.14/using/cmdline.html#cmdoption-X) or after setting the [PYTHON_GIL=0](https://docs.python.org/3.14/using/cmdline.html#envvar-PYTHON_GIL)
environment variable. This feature enables improved performance for
multi-threaded applications and makes it easier to use multi-core CPUs
efficiently. For more details, see [PEP 703](https://peps.python.org/pep-0703/).

In prior versions of Python’s C API, a function might declare that it
requires the GIL to be held in order to use it. This refers to having an
[attached thread state](../attached-thread-state/index.md).
