# [bytecode](https://docs.python.org/3.14/glossary.html#term-bytecode)

Python source code is compiled into bytecode, the internal representation of a Python program in the CPython interpreter.  The bytecode is also cached in `.pyc` files so that executing the same file is faster the second time (recompilation from source to bytecode can be avoided).  This “intermediate language” is said to run on a [virtual machine](../virtual-machine/index.md) that executes the machine code corresponding to each bytecode. Do note that bytecodes are not expected to work between different Python virtual machines, nor to be stable between Python releases.

A list of bytecode instructions can be found in the documentation for [the dis module](https://docs.python.org/3.14/library/dis.html#bytecodes).
