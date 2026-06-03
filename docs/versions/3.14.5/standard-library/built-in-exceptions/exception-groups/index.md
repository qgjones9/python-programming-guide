# [Exception groups](https://docs.python.org/3/library/exceptions.html#exception-groups)

The following are used when it is necessary to raise multiple unrelated exceptions. They are part of the exception hierarchy so they can be handled with `except` like all other exceptions. In addition, they are recognised by `except*`, which matches their subgroups based on the types of the contained exceptions.

Both `ExceptionGroup` and `BaseExceptionGroup` wrap the exceptions in a sequence. The difference is that `BaseExceptionGroup` extends `BaseException` and can wrap any exception, while `ExceptionGroup` extends `Exception` and can only wrap subclasses of `Exception`. This design is so that `except Exception` catches an `ExceptionGroup` but not a `BaseExceptionGroup`.

## Table of contents

Mirrors the official Python 3 library index for this section. Each link opens a stub page whose H1 links to the canonical docs.

| Exception | Description |
|-----------|-------------|
| [ExceptionGroup](exceptiongroup/index.md) | Wraps multiple `Exception` subclasses; handled by `except Exception` and `except*`. |
| [BaseExceptionGroup](baseexceptiongroup/index.md) | Wraps any exception type; extends `BaseException`; constructor may return `ExceptionGroup` when all contained exceptions are `Exception` instances. |
