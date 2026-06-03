# [thread state](https://docs.python.org/3.14/glossary.html#term-thread-state)

The information used by the [CPython](../CPython/index.md) runtime to run in an OS thread. For example, this includes the current exception, if any, and the state of the bytecode interpreter.

Each thread state is bound to a single OS thread, but threads may have many thread states available.  At most, one of them may be [attached](../attached-thread-state/index.md) at once.

An [attached thread state](../attached-thread-state/index.md) is required to call most of Python’s C API, unless a function explicitly documents otherwise. The bytecode interpreter only runs under an attached thread state.

Each thread state belongs to a single interpreter, but each interpreter may have many thread states, including multiple for the same OS thread. Thread states from multiple interpreters may be bound to the same thread, but only one can be [attached](../attached-thread-state/index.md) in that thread at any given moment.

See [Thread State and the Global Interpreter Lock](https://docs.python.org/3.14/c-api/threads.html#threads) for more information.

