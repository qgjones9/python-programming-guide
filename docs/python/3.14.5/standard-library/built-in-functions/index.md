# [Built-in Functions](https://docs.python.org/3/library/functions.html)

Local notes keyed to the official documentation: Built-in Functions.

## Table of contents

Mirrors the official Python 3 library index for this section. Each link opens a stub page whose H1 links to the canonical docs.

| Function | Description |
|----------|-------------|
| [__import__()](import/index.md) | Low-level hook invoked by the `import` statement; prefer `importlib.import_module`. |
| [abs()](abs/index.md) | Returns the absolute value of a number, or the magnitude when the argument is complex. |
| [aiter()](aiter/index.md) | Returns an asynchronous iterator from an async iterable, equivalent to calling __aiter__(). |
| [all()](all/index.md) | Returns True when every element of the iterable is truthy, including vacuously for an empty iterable. |
| [anext()](anext/index.md) | Awaits and returns the next item from an async iterator, with an optional default when exhausted. |
| [any()](any/index.md) | Returns True when at least one element of the iterable is truthy, otherwise False for an empty iterable. |
| [ascii()](ascii/index.md) | Returns a repr-style ASCII-safe string with non-ASCII characters escaped via \x, \u, or \U sequences. |
| [bin()](bin/index.md) | Converts an integer to a binary string literal prefixed with 0b that can be evaluated as Python code. |
| [bool()](bool/index.md) | Converts a value to True or False using Python's standard truth-testing procedure. |
| [breakpoint()](breakpoint/index.md) | Enters the debugger at the call site by invoking sys.breakpointhook(), defaulting to pdb.set_trace(). |
| [bytearray()](bytearray/index.md) | Creates a mutable array of byte values in the range 0–255 from an optional source. |
| [bytes()](bytes/index.md) | Creates an immutable sequence of byte values from an integer size, iterable, buffer, or encoded string. |
| [callable()](callable/index.md) | Reports whether an object appears callable, including functions, classes, and instances with __call__(). |
| [chr()](chr/index.md) | Returns the one-character string for a Unicode code point from 0 through 0x10FFFF. |
| [classmethod()](classmethod/index.md) | Decorator that binds a method to the class, passing the class object as the first argument instead of self. |
| [compile()](compile/index.md) | Compiles source code into a code object suitable for exec() or eval() with a chosen execution mode. |
| [complex()](complex/index.md) | Constructs a complex number from numeric or string input, or from separate real and imaginary parts. |
| [delattr()](delattr/index.md) | Deletes a named attribute from an object when deletion is permitted, equivalent to del object.name. |
| [dict()](dict/index.md) | Creates a dictionary from keyword arguments, an existing mapping, or an iterable of key-value pairs. |
| [dir()](dir/index.md) | Returns a sorted list of names in the current local scope, or valid attribute names for a given object. |
| [divmod()](divmod/index.md) | Takes two numbers and returns a tuple of their quotient and remainder from integer division. |
| [enumerate()](enumerate/index.md) | Returns an iterator of `(index, value)` pairs while looping over any iterable, with an optional start index. |
| [eval()](eval/index.md) | Parses and evaluates a Python expression from a string (or code object) using optional global and local namespaces. |
| [exec()](exec/index.md) | Dynamically executes Python statements from a string or compiled code object in optional global and local namespaces. |
| [filter()](filter/index.md) | Builds an iterator of elements from an iterable for which a predicate function returns true; with `None`, keeps truthy values. |
| [float()](float/index.md) | Constructs a floating-point number from another number, a numeric string, or an object implementing `__float__()` or `__index__()`. |
| [format()](format/index.md) | Converts a value to a formatted string according to a format specification, delegating to `type(value).__format__()`. |
| [frozenset()](frozenset/index.md) | Returns an immutable set built from an optional iterable; supports set operations but cannot be modified after creation. |
| [getattr()](getattr/index.md) | Returns the value of a named attribute on an object; with a default, returns that instead of raising `AttributeError`. |
| [globals()](globals/index.md) | Returns the dictionary implementing the current module namespace (global variables visible at the call site). |
| [hasattr()](hasattr/index.md) | Returns `True` if the object has the named attribute, otherwise `False` (implemented via `getattr` and `AttributeError`). |
| [hash()](hash/index.md) | Returns the integer hash value of an object, used for fast dict and set lookups; equal objects must have equal hashes. |
| [help()](help/index.md) | Invokes the interactive help system for modules, functions, classes, keywords, or any object with documentation. |
| [hex()](hex/index.md) | Converts an integer to a lowercase hexadecimal string prefixed with `0x`. |
| [id()](id/index.md) | Returns an integer identity for an object, unique among simultaneously live objects (in CPython, typically the memory address). |
| [input()](input/index.md) | Reads a line from standard input as a string, optionally writing a prompt to stdout first. |
| [int()](int/index.md) | Constructs an integer from a number, a string in a given base, or objects implementing `__int__()` / `__index__()`. |
| [isinstance()](isinstance/index.md) | Returns True when an object is an instance of a class or any of several types. |
| [issubclass()](issubclass/index.md) | Returns True when a class is a subclass of another class or any type in a tuple. |
| [iter()](iter/index.md) | Returns an iterator over an iterable, or repeatedly calls a callable until a sentinel. |
| [len()](len/index.md) | Returns the number of items in a sequence or collection. |
| [list()](list/index.md) | Creates a mutable ordered sequence, optionally copied from an iterable. |
| [locals()](locals/index.md) | Returns a mapping of local variable names to their current values. |
| [map()](map/index.md) | Applies a function to each item of one or more iterables, yielding results lazily. |
| [max()](max/index.md) | Returns the largest item in an iterable or the largest of two or more arguments. |
| [memoryview()](memoryview/index.md) | Creates a zero-copy view over a buffer-supporting object's binary data. |
| [min()](min/index.md) | Returns the smallest item in an iterable or the smallest of two or more arguments. |
| [next()](next/index.md) | Retrieves the next item from an iterator, with an optional default if exhausted. |
| [object()](object/index.md) | The ultimate base class for all Python classes; returns a featureless instance. |
| [oct()](oct/index.md) | Converts an integer to an octal string prefixed with 0o. |
| [open()](open/index.md) | Opens a file and returns a file object for reading, writing, or updating. |
| [ord()](ord/index.md) | Returns the Unicode code point for a one-character string, or a byte value for length-1 bytes. |
| [pow()](pow/index.md) | Raises base to exp, optionally modulo mod; supports efficient modular exponentiation. |
| [print()](print/index.md) | Writes objects as text to a stream, separated by sep and terminated with end. |
| [property()](property/index.md) | Defines managed attributes with getter, setter, deleter, and optional docstring. |
| [range()](range/index.md) | Immutable sequence of evenly spaced integers for memory-efficient loops and indexing. |
| [repr()](repr/index.md) | Returns an unambiguous, often evaluable string representation of an object. |
| [reversed()](reversed/index.md) | Returns a reverse iterator over a sequence or object with `__reversed__`. |
| [round()](round/index.md) | Rounds a number to the nearest integer or to a given decimal precision. |
| [set()](set/index.md) | Creates a mutable unordered collection of unique hashable elements. |
| [setattr()](setattr/index.md) | Assigns a named attribute on an object, equivalent to `obj.name = value`. |
| [slice()](slice/index.md) | Builds a reusable slice object for extended indexing (`start:stop:step`). |
| [sorted()](sorted/index.md) | Returns a new list containing items from an iterable in ascending order. |
| [staticmethod()](staticmethod/index.md) | Converts a function into a static method that does not receive `self` or `cls`. |
| [str()](str/index.md) | Constructs a text string from an object or decodes bytes with an encoding. |
| [sum()](sum/index.md) | Adds items of an iterable left to right, with an optional start value. |
| [super()](super/index.md) | Returns a proxy to invoke methods on parent or sibling classes in the MRO. |
| [tuple()](tuple/index.md) | Creates an immutable sequence, often used for fixed records and unpacking. |
| [type()](type/index.md) | Returns an object's type or dynamically constructs a new class from name, bases, and dict. |
| [vars()](vars/index.md) | Returns the `__dict__` namespace of a module, class, or instance. |
| [zip()](zip/index.md) | Iterates several iterables in parallel, yielding tuples of aligned items. |
