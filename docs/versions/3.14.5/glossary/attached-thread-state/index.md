# [attached thread state](https://docs.python.org/3.14/glossary.html#term-attached-thread-state)

A [thread state](../thread-state/index.md) that is active for the current OS thread.

When a [thread state](../thread-state/index.md) is attached, the OS thread has
access to the full Python C API and can safely invoke the
bytecode interpreter.

Unless a function explicitly notes otherwise, attempting to call
the C API without an attached thread state will result in a fatal
error or undefined behavior.  A thread state can be attached and detached
explicitly by the user through the C API, or implicitly by the runtime,
including during blocking C calls and by the bytecode interpreter in between
calls.

On most builds of Python, having an attached thread state implies that the
caller holds the [GIL](../GIL/index.md) for the current interpreter, so only
one OS thread can have an attached thread state at a given moment. In
[free-threaded builds](../free-threaded-build/index.md) of Python, threads can
concurrently hold an attached thread state, allowing for true parallelism of
the bytecode interpreter.
