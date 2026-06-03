# [Inheriting from built-in exceptions](https://docs.python.org/3/library/exceptions.html#inheriting-from-built-in-exceptions)

User code can create subclasses that inherit from an exception type. It’s recommended to only subclass one exception type at a time to avoid any possible conflicts between how the bases handle the `args` attribute, as well as due to possible memory layout incompatibilities.

**CPython implementation detail:** Most built-in exceptions are implemented in C for efficiency (see `Objects/exceptions.c`). Some have custom memory layouts which makes it impossible to create a subclass that inherits from multiple exception types. The memory layout of a type is an implementation detail and might change between Python versions, leading to new conflicts in the future. Therefore, it’s recommended to avoid subclassing multiple exception types altogether.

Programmers are encouraged to derive new exceptions from the `Exception` class or one of its subclasses, and not from `BaseException`.
