# [bytes-like object](https://docs.python.org/3.14/glossary.html#term-bytes-like-object)

An object that supports the [Buffer Protocol](https://docs.python.org/3.14/c-api/buffer.html#bufferobjects) and can
export a C-[contiguous](../contiguous/index.md) buffer. This includes all [bytes](https://docs.python.org/3.14/library/stdtypes.html#bytes),
[bytearray](https://docs.python.org/3.14/library/stdtypes.html#bytearray), and [array.array](https://docs.python.org/3.14/library/array.html#array.array) objects, as well as many
common [memoryview](https://docs.python.org/3.14/library/stdtypes.html#memoryview) objects.  Bytes-like objects can
be used for various operations that work with binary data; these include
compression, saving to a binary file, and sending over a socket.

Some operations need the binary data to be mutable.  The documentation
often refers to these as “read-write bytes-like objects”.  Example
mutable buffer objects include [bytearray](https://docs.python.org/3.14/library/stdtypes.html#bytearray) and a
[memoryview](https://docs.python.org/3.14/library/stdtypes.html#memoryview) of a `bytearray`.
Other operations require the binary data to be stored in
immutable objects (“read-only bytes-like objects”); examples
of these include [bytes](https://docs.python.org/3.14/library/stdtypes.html#bytes) and a `memoryview`
of a `bytes` object.
