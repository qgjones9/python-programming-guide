# [Concrete exceptions](https://docs.python.org/3/library/exceptions.html#concrete-exceptions)

Local notes keyed to the official documentation: Concrete exceptions.

## Table of contents

Mirrors the official Python 3 library index for this section. Each link opens a stub page whose H1 links to the canonical docs.

| Exception | Description |
|-----------|-------------|
| [AssertionError](assertionerror/index.md) | Raised when an `assert` statement fails. |
| [AttributeError](attributeerror/index.md) | Raised when an attribute reference or assignment fails on an object. |
| [EOFError](eoferror/index.md) | Raised when `input()` hits end-of-file without reading any data. |
| [FloatingPointError](floatingpointerror/index.md) | Base class for floating-point arithmetic errors; not currently used by the interpreter. |
| [GeneratorExit](generatorexit/index.md) | Raised when a generator or coroutine is closed; inherits from `BaseException`, not `Exception`. |
| [ImportError](importerror/index.md) | Raised when the `import` statement cannot load a module or resolve a name in `from … import`. |
| [ModuleNotFoundError](modulenotfounderror/index.md) | Subclass of `ImportError` raised when a module cannot be located or is `None` in `sys.modules`. |
| [IndexError](indexerror/index.md) | Raised when a sequence subscript is out of range. |
| [KeyError](keyerror/index.md) | Raised when a mapping key is not found among existing keys. |
| [KeyboardInterrupt](keyboardinterrupt/index.md) | Raised when the user presses the interrupt key (typically Control-C); inherits from `BaseException`. |
| [MemoryError](memoryerror/index.md) | Raised when an operation runs out of memory but recovery may still be possible. |
| [NameError](nameerror/index.md) | Raised when a local or global name is not found (unqualified names only). |
| [NotImplementedError](notimplementederror/index.md) | Subclass of `RuntimeError` for abstract methods that subclasses must override. |
| [OSError](oserror/index.md) | Raised for system-related errors, including I/O failures such as missing files or full disks. |
| [OverflowError](overflowerror/index.md) | Raised when an arithmetic result is too large to represent (not for integer overflow in normal use). |
| [PythonFinalizationError](pythonfinalizationerror/index.md) | Subclass of `RuntimeError` raised when an operation is blocked during interpreter shutdown. |
| [RecursionError](recursionerror/index.md) | Subclass of `RuntimeError` raised when maximum recursion depth is exceeded. |
| [ReferenceError](referenceerror/index.md) | Raised when a weak-reference proxy accesses an attribute after the referent is collected. |
| [RuntimeError](runtimeerror/index.md) | Raised for errors that do not fit any more specific built-in exception category. |
| [StopIteration](stopiteration/index.md) | Raised by `next()` and `__next__()` to signal that an iterator is exhausted. |
| [StopAsyncIteration](stopasynciteration/index.md) | Must be raised by an async iterator's `__anext__()` to stop asynchronous iteration. |
| [SyntaxError](syntaxerror/index.md) | Raised when the parser encounters invalid syntax during import, compile, exec, eval, or startup. |
| [IndentationError](indentationerror/index.md) | Subclass of `SyntaxError` for syntax errors caused by incorrect indentation. |
| [TabError](taberror/index.md) | Subclass of `IndentationError` for inconsistent mixing of tabs and spaces in indentation. |
| [SystemError](systemerror/index.md) | Raised when the interpreter detects an internal error that is not considered fatal. |
| [SystemExit](systemexit/index.md) | Raised by `sys.exit()` to terminate the interpreter; inherits from `BaseException`. |
| [TypeError](typeerror/index.md) | Raised when an operation or function is applied to an object of inappropriate type. |
| [UnboundLocalError](unboundlocalerror/index.md) | Subclass of `NameError` raised when a local variable is referenced before assignment. |
| [UnicodeError](unicodeerror/index.md) | Subclass of `ValueError` for Unicode encoding or decoding failures. |
| [UnicodeEncodeError](unicodeencodeerror/index.md) | Subclass of `UnicodeError` raised during Unicode encoding. |
| [UnicodeDecodeError](unicodedecodeerror/index.md) | Subclass of `UnicodeError` raised during Unicode decoding. |
| [UnicodeTranslateError](unicodetranslateerror/index.md) | Subclass of `UnicodeError` raised during Unicode translation between codecs. |
| [ValueError](valueerror/index.md) | Raised when an argument has the correct type but an inappropriate value. |
| [ZeroDivisionError](zerodivisionerror/index.md) | Raised when the divisor or modulo operand is zero. |
| [EnvironmentError](environmenterror/index.md) | Compatibility alias of `OSError` retained since Python 3.3. |
| [IOError](ioerror/index.md) | Compatibility alias of `OSError` retained since Python 3.3. |
| [WindowsError](windowserror/index.md) | Windows-only compatibility alias of `OSError` retained since Python 3.3. |
