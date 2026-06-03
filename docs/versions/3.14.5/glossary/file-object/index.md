# [file object](https://docs.python.org/3.14/glossary.html#term-file-object)

An object exposing a file-oriented API (with methods such as `read()` or `write()`) to an underlying resource.  Depending on the way it was created, a file object can mediate access to a real on-disk file or to another type of storage or communication device (for example standard input/output, in-memory buffers, sockets, pipes, etc.).  File objects are also called *file-like objects* or

*streams*.

There are actually three categories of file objects: raw [binary files](../binary-file/index.md), buffered binary files and [text files](../text-file/index.md).

Their interfaces are defined in the [io](https://docs.python.org/3.14/library/io.html#module-io) module.  The canonical way to create a file object is by using the [open()](https://docs.python.org/3.14/library/functions.html#open) function.
