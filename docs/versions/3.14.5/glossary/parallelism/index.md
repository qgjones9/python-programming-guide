# [parallelism](https://docs.python.org/3.14/glossary.html#term-parallelism)

Executing multiple operations at the same time (e.g. on multiple CPU
cores).  In Python builds with the
[global interpreter lock (GIL)](../global-interpreter-lock/index.md), only one
thread runs Python bytecode at a time, so taking advantage of multiple
CPU cores typically involves multiple processes
(e.g. [multiprocessing](https://docs.python.org/3.14/library/multiprocessing.html#module-multiprocessing)) or native extensions that release the GIL.
In [free-threaded](../free-threading/index.md) Python, multiple Python threads
can run Python code simultaneously on different cores.
