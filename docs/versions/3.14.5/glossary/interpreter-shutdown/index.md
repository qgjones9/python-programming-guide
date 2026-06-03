# [interpreter shutdown](https://docs.python.org/3.14/glossary.html#term-interpreter-shutdown)

When asked to shut down, the Python interpreter enters a special phase
where it gradually releases all allocated resources, such as modules
and various critical internal structures.  It also makes several calls
to the [garbage collector](../garbage-collection/index.md). This can trigger
the execution of code in user-defined destructors or weakref callbacks.
Code executed during the shutdown phase can encounter various
exceptions as the resources it relies on may not function anymore
(common examples are library modules or the warnings machinery).

The main reason for interpreter shutdown is that the `__main__` module
or the script being run has finished executing.
