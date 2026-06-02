#!/usr/bin/env python3
"""Generate batch 3/4 built-in function enrichment pages (isinstance through property)."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/python/3.14.5/standard-library/built-in-functions"

PAGES: dict[str, dict[str, str]] = {
    "isinstance": {
        "h1": "# [isinstance()](https://docs.python.org/3/library/functions.html#isinstance)",
        "short": "Returns True when an object is an instance of a class or any of several types.",
        "body": textwrap.dedent(
            """
            ## Description

            `isinstance(object, classinfo)` tests whether `object` is an instance of `classinfo`, or of a direct, indirect, or virtual subclass. `classinfo` may be a type, a tuple of types, or a union type.

            ## What problem it solves

            Runtime type checks that respect inheritance—validating API inputs, branching on supported types, or guarding conversions without brittle `type(x) is T` comparisons.

            ## Implementation options

            ### Check a single type

            ```python
            assert isinstance(42, int)
            assert isinstance("hi", str)
            assert not isinstance(3.14, int)
            ```

            ### Accept several types with a tuple

            ```python
            def stringify(value):
                if not isinstance(value, (str, int, float)):
                    raise TypeError("expected str, int, or float")
                return str(value)

            assert stringify(99) == "99"
            assert stringify(3.5) == "3.5"
            ```

            ### Subclasses match the base type

            ```python
            class AdminUser:
                pass

            user = AdminUser()
            assert isinstance(user, AdminUser)
            assert isinstance(user, object)
            ```

            ## Best practices

            - Prefer `isinstance()` over `type(x) is T` when subclasses should be accepted.
            - Avoid excessive isinstance chains—consider duck typing or a single protocol check.
            - Use union types or tuples for “one of several types” rather than nested if/else.
            """
        ).strip(),
    },
    "issubclass": {
        "h1": "# [issubclass()](https://docs.python.org/3/library/functions.html#issubclass)",
        "short": "Returns True when a class is a subclass of another class or any type in a tuple.",
        "body": textwrap.dedent(
            """
            ## Description

            `issubclass(class, classinfo)` returns `True` if `class` is a subclass of `classinfo`. A class is considered a subclass of itself. `classinfo` may be a tuple of classes or a union type.

            ## What problem it solves

            Framework and plugin code needs to verify inheritance relationships—whether a registered class extends a base API, or whether metaclass hooks apply.

            ## Implementation options

            ### Direct and indirect inheritance

            ```python
            class Animal:
                pass

            class Dog(Animal):
                pass

            assert issubclass(Dog, Animal)
            assert issubclass(Dog, Dog)
            assert not issubclass(Animal, Dog)
            ```

            ### Test against several allowed bases

            ```python
            class Serializer:
                pass

            class JsonSerializer(Serializer):
                pass

            allowed = (Serializer, type(None))
            assert issubclass(JsonSerializer, allowed)
            ```

            ### Contrast with isinstance on instances

            ```python
            class A:
                pass

            class B(A):
                pass

            obj = B()
            assert isinstance(obj, A)
            assert issubclass(B, A)
            ```

            ## Best practices

            - Use `issubclass` on classes, `isinstance` on instances—do not mix them up.
            - Remember every class is a subclass of `object` unless you are using old-style patterns.
            - For structural typing, consider `typing.Protocol` instead of inheritance checks alone.
            """
        ).strip(),
    },
    "iter": {
        "h1": "# [iter()](https://docs.python.org/3/library/functions.html#iter)",
        "short": "Returns an iterator over an iterable, or repeatedly calls a callable until a sentinel.",
        "body": textwrap.dedent(
            """
            ## Description

            With one argument, `iter(iterable)` returns an iterator object. With two arguments, `iter(callable, sentinel)` calls `callable` with no arguments until the return value equals `sentinel`.

            ## What problem it solves

            Manual iteration starts with obtaining an iterator—whether from a collection or from repeated reads (fixed-size blocks, polling until done).

            ## Implementation options

            ### Iterator from a list

            ```python
            it = iter([10, 20, 30])
            assert next(it) == 10
            assert list(it) == [20, 30]
            ```

            ### Callable plus sentinel for block reads

            ```python
            from io import BytesIO

            data = BytesIO(b"abcdefgh")
            blocks = list(iter(lambda: data.read(3), b""))
            assert blocks == [b"abc", b"def", b"gh"]
            ```

            ### Strings are iterable but not always iterators

            ```python
            word = "abc"
            assert list(iter(word)) == ["a", "b", "c"]
            ```

            ## Best practices

            - Prefer `for item in iterable` when you do not need the iterator object itself.
            - The two-argument form is ideal for reading chunks until EOF without a while loop.
            - Remember `iter()` on a generator returns the same generator object, not a fresh copy.
            """
        ).strip(),
    },
    "len": {
        "h1": "# [len()](https://docs.python.org/3/library/functions.html#len)",
        "short": "Returns the number of items in a sequence or collection.",
        "body": textwrap.dedent(
            """
            ## Description

            `len(object)` returns the length—the number of items—of a sequence or collection. Custom types may implement `__len__()` to participate.

            ## What problem it solves

            Bounds checks, progress reporting, validating input size, and choosing algorithms that depend on how many elements you have.

            ## Implementation options

            ### Common built-in types

            ```python
            assert len([1, 2, 3]) == 3
            assert len("hello") == 5
            assert len({"a": 1, "b": 2}) == 2
            assert len({1, 2, 3}) == 3
            ```

            ### Custom container with `__len__`

            ```python
            class Queue:
                def __init__(self, items):
                    self._items = list(items)

                def __len__(self):
                    return len(self._items)

            assert len(Queue(["x", "y"])) == 2
            ```

            ### Empty versus non-empty checks

            ```python
            pending = []
            assert len(pending) == 0
            if not pending:
                pending.append("task")
            assert len(pending) == 1
            ```

            ## Best practices

            - For emptiness tests, `if not seq:` is idiomatic; use `len` when you need the actual count.
            - `len()` is O(1) for list, tuple, str, dict, and set in CPython.
            - Very large theoretical ranges may raise `OverflowError`—rare in everyday code.
            """
        ).strip(),
    },
    "list": {
        "h1": "# [list()](https://docs.python.org/3/library/functions.html#func-list)",
        "short": "Creates a mutable ordered sequence, optionally copied from an iterable.",
        "body": textwrap.dedent(
            """
            ## Description

            `list()` returns a new list. With an iterable argument, it copies elements into a mutable sequence. `list` is a built-in type supporting append, extend, sort, and more.

            ## What problem it solves

            You need an ordered, changeable collection—accumulating results, reordering data, or materializing an iterator for reuse.

            ## Implementation options

            ### Empty list and literal equivalent

            ```python
            empty = list()
            assert empty == []
            ```

            ### Copy from an iterable

            ```python
            assert list("abc") == ["a", "b", "c"]
            assert list((1, 2)) == [1, 2]
            assert sorted(list({3, 1, 2})) == [1, 2, 3]
            ```

            ### Build from a generator expression

            ```python
            squares = list(x * x for x in range(5))
            assert squares == [0, 1, 4, 9, 16]
            ```

            ## Best practices

            - Use `[]` for empty lists in application code; `list()` is useful when shadowing hides the name `list`.
            - `list(iterable)` copies—mutating the list does not affect the source iterable.
            - For large streams, consider keeping a generator instead of materializing everything.
            """
        ).strip(),
    },
    "locals": {
        "h1": "# [locals()](https://docs.python.org/3/library/functions.html#locals)",
        "short": "Returns a mapping of local variable names to their current values.",
        "body": textwrap.dedent(
            """
            ## Description

            `locals()` returns a mapping object representing the current local symbol table. At module scope (and in some exec/eval contexts) it may match `globals()`. Behavior in optimized scopes (functions) returns a snapshot whose updates may not write back to local variables.

            ## What problem it solves

            Debugging, templating, and dynamic execution need to inspect or copy the names bound in the current scope.

            ## Implementation options

            ### Inspect bindings inside a function

            ```python
            def demo():
                x = 10
                y = "ok"
                return locals()

            snap = demo()
            assert snap["x"] == 10
            assert snap["y"] == "ok"
            ```

            ### Format a simple template from local names

            ```python
            def render():
                title = "Report"
                count = 3
                return f"{title}: {count} items"

            assert render() == "Report: 3 items"
            ```

            ### Read keys from a snapshot

            ```python
            def demo():
                a = 1
                b = 2
                return sorted(locals())

            assert demo() == ["a", "b"]
            ```

            ## Best practices

            - Do not rely on mutating `locals()` to change function variables in optimized scopes (PEP 667).
            - Prefer explicit parameters and return values over magic locals inspection in production code.
            - Use `locals()` mainly for debuggers, REPL tooling, and framework introspection.
            """
        ).strip(),
    },
    "map": {
        "h1": "# [map()](https://docs.python.org/3/library/functions.html#map)",
        "short": "Applies a function to each item of one or more iterables, yielding results lazily.",
        "body": textwrap.dedent(
            """
            ## Description

            `map(function, iterable, /, *iterables, strict=False)` returns an iterator that applies `function` to each item. With multiple iterables, `function` receives parallel items and iteration stops at the shortest unless `strict=True`.

            ## What problem it solves

            Transform every element of a sequence—parse strings to ints, normalize records, combine parallel columns—without an explicit index loop.

            ## Implementation options

            ### Map a function over one iterable

            ```python
            nums = ["1", "2", "3"]
            assert list(map(int, nums)) == [1, 2, 3]
            ```

            ### Map with multiple iterables

            ```python
            widths = [2, 3, 4]
            heights = [5, 6, 7]
            areas = list(map(lambda w, h: w * h, widths, heights))
            assert areas == [10, 18, 28]
            ```

            ### Parallel iterables stop at the shortest

            ```python
            a = list(map(lambda x, y: x + y, [1, 2, 3], [10, 20]))
            assert a == [11, 22]
            ```

            ## Best practices

            - A list comprehension is often clearer for simple transforms; `map` shines with an existing function like `int`.
            - `map` returns an iterator—consume once or wrap with `list()`.
            - In Python 3.14+, `strict=True` raises when parallel iterables differ in length.
            """
        ).strip(),
    },
    "max": {
        "h1": "# [max()](https://docs.python.org/3/library/functions.html#max)",
        "short": "Returns the largest item in an iterable or the largest of two or more arguments.",
        "body": textwrap.dedent(
            """
            ## Description

            `max()` returns the largest item. With one iterable argument, it scans for the maximum. With multiple positional arguments, it compares them directly. Optional `key` and `default` keyword arguments customize ordering and empty-input behavior.

            ## What problem it solves

            Finding peaks—latest timestamp, highest score, biggest file—without writing manual comparison loops.

            ## Implementation options

            ### Maximum of an iterable

            ```python
            scores = [88, 92, 75, 92]
            assert max(scores) == 92
            ```

            ### Compare several values directly

            ```python
            assert max(3, 9, 1) == 9
            ```

            ### Use key= for derived ordering

            ```python
            words = ["Banana", "apple", "Cherry"]
            assert max(words, key=str.lower) == "Cherry"
            ```

            ## Best practices

            - Provide `default=` when the iterable may be empty to avoid `ValueError`.
            - When several items tie for max, the first encountered wins (stable behavior).
            - For repeated max operations on a changing heap, consider `heapq.nlargest`.
            """
        ).strip(),
    },
    "memoryview": {
        "h1": "# [memoryview()](https://docs.python.org/3/library/functions.html#func-memoryview)",
        "short": "Creates a zero-copy view over a buffer-supporting object's binary data.",
        "body": textwrap.dedent(
            """
            ## Description

            `memoryview(object)` returns a memory view over bytes-like or buffer-exporting objects. Views expose slicing and casting without copying the underlying buffer.

            ## What problem it solves

            Efficient binary I/O, parsing protocols, and sharing large byte buffers between libraries without duplicating memory.

            ## Implementation options

            ### Slice a bytes object without copying

            ```python
            data = bytearray(b"hello world")
            view = memoryview(data)
            chunk = view[6:11]
            assert bytes(chunk) == b"world"
            ```

            ### Mutate through a view

            ```python
            buf = bytearray(b"abc")
            mv = memoryview(buf)
            mv[0] = ord("x")
            assert buf == bytearray(b"xbc")
            ```

            ### Release the view before resizing the buffer

            ```python
            payload = bytearray(b"1234")
            view = memoryview(payload)
            view.release()
            payload.append(5)
            assert len(payload) == 5
            ```

            ## Best practices

            - Call `release()` on views when done if the underlying buffer may be resized or freed.
            - Prefer `memoryview` for parsing fixed binary layouts over repeated slicing that copies.
            - Not all buffer operations allow mutation—check `readonly` on the view when writing.
            """
        ).strip(),
    },
    "min": {
        "h1": "# [min()](https://docs.python.org/3/library/functions.html#min)",
        "short": "Returns the smallest item in an iterable or the smallest of two or more arguments.",
        "body": textwrap.dedent(
            """
            ## Description

            `min()` returns the smallest item. With one iterable, it scans for the minimum; with multiple arguments, it compares them directly. Supports optional `key` and `default` like `max()`.

            ## What problem it solves

            Finding lower bounds—earliest date, cheapest option, closest match threshold—in one readable call.

            ## Implementation options

            ### Minimum of a list

            ```python
            temps = [72, 68, 75, 65]
            assert min(temps) == 65
            ```

            ### Compare multiple scalars

            ```python
            assert min(10, 3, 7) == 3
            ```

            ### key= for custom ordering

            ```python
            records = [("Ada", 36), ("Grace", 45)]
            youngest = min(records, key=lambda r: r[1])
            assert youngest == ("Ada", 36)
            ```

            ## Best practices

            - Use `default=` when the iterable might be empty.
            - Ties return the first minimal element encountered.
            - For complex selection (top-k), use `heapq.nsmallest` instead of sorting the whole iterable.
            """
        ).strip(),
    },
    "next": {
        "h1": "# [next()](https://docs.python.org/3/library/functions.html#next)",
        "short": "Retrieves the next item from an iterator, with an optional default if exhausted.",
        "body": textwrap.dedent(
            """
            ## Description

            `next(iterator, default=None)` calls the iterator's `__next__()` method. Without `default`, exhausted iterators raise `StopIteration`; with `default`, that value is returned instead.

            ## What problem it solves

            Manual iterator control—pull one item at a time, peek-adjacent patterns, or safe iteration when exhaustion is expected.

            ## Implementation options

            ### Advance an iterator step by step

            ```python
            it = iter([1, 2, 3])
            assert next(it) == 1
            assert next(it) == 2
            assert next(it) == 3
            ```

            ### Default when iterator is empty

            ```python
            it = iter([])
            assert next(it, None) is None
            assert next(it, "done") == "done"
            ```

            ### Manual loop using next

            ```python
            it = iter(["a", "b"])
            items = []
            while True:
                item = next(it, None)
                if item is None:
                    break
                items.append(item)
            assert items == ["a", "b"]
            ```

            ## Best practices

            - Prefer `for` loops for full iteration; use `next()` for streaming or parser-style logic.
            - Always provide `default` when exhaustion is normal, not exceptional.
            - Do not catch `StopIteration` outside generator protocol code—it has special meaning inside generators.
            """
        ).strip(),
    },
    "object": {
        "h1": "# [object()](https://docs.python.org/3/library/functions.html#object)",
        "short": "The ultimate base class for all Python classes; returns a featureless instance.",
        "body": textwrap.dedent(
            """
            ## Description

            `object()` returns a new featureless object—the root of Python's class hierarchy. All classes inherit from `object`. Instances of bare `object()` have no `__dict__` and cannot receive arbitrary attributes.

            ## What problem it solves

            Understanding inheritance, creating minimal sentinel instances, and anchoring the type system—every user-defined class ultimately derives from `object`.

            ## Implementation options

            ### Create a unique sentinel

            ```python
            MISSING = object()
            cache = {}

            def get(key, default=MISSING):
                if key in cache:
                    return cache[key]
                if default is not MISSING:
                    return default
                raise KeyError(key)

            assert get("x", default=0) == 0
            ```

            ### All classes subclass object

            ```python
            class Widget:
                pass

            assert issubclass(Widget, object)
            assert isinstance(Widget(), object)
            ```

            ### Bare object rejects arbitrary attributes

            ```python
            bare = object()
            try:
                bare.x = 1
                raised = False
            except AttributeError:
                raised = True
            assert raised
            ```

            ## Best practices

            - Use a unique `object()` sentinel instead of `None` when `None` is valid data.
            - Subclass `object` explicitly only when teaching—in Python 3 it is implicit.
            - For rich instances, define a proper class instead of using bare `object()`.
            """
        ).strip(),
    },
    "oct": {
        "h1": "# [oct()](https://docs.python.org/3/library/functions.html#oct)",
        "short": "Converts an integer to an octal string prefixed with 0o.",
        "body": textwrap.dedent(
            """
            ## Description

            `oct(integer)` converts an integer to a lowercase octal string with an `0o` prefix. Non-integers must define `__index__()`. The result is a valid Python literal.

            ## What problem it solves

            Debugging low-level values, Unix file permissions, and teaching base-8 representation without manual division loops.

            ## Implementation options

            ### Positive and negative integers

            ```python
            assert oct(8) == "0o10"
            assert oct(-8) == "-0o10"
            ```

            ### Round-trip with int(base=8)

            ```python
            text = oct(511)
            assert int(text, 8) == 511
            ```

            ### File mode style bitmask

            ```python
            mode = 0o755
            assert oct(mode) == "0o755"
            assert int("755", 8) == 493
            ```

            ## Best practices

            - Use `format(n, "o")` or f-strings when you need octal without the `0o` prefix.
            - Remember Python 3 uses `0o` prefix; do not confuse with old C-style leading zero literals.
            - For user-facing output, label the base explicitly so values are not misread as decimal.
            """
        ).strip(),
    },
    "open": {
        "h1": "# [open()](https://docs.python.org/3/library/functions.html#open)",
        "short": "Opens a file and returns a file object for reading, writing, or updating.",
        "body": textwrap.dedent(
            """
            ## Description

            `open(file, mode='r', encoding=None, ...)` returns a file object. Text mode (default) decodes bytes to `str`; binary mode (`'rb'`, `'wb'`) works with `bytes`. Context managers (`with open(...)`) ensure files close reliably.

            ## What problem it solves

            Reading configuration, writing logs, and processing data on disk—the primary interface between Python programs and the filesystem.

            ## Implementation options

            ### Read a text file

            ```python
            from pathlib import Path
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "sample.txt"
                path.write_text("line1\\nline2\\n", encoding="utf-8")
                with open(path, encoding="utf-8") as f:
                    lines = f.read().splitlines()
                assert lines == ["line1", "line2"]
            ```

            ### Write binary data

            ```python
            import tempfile
            from pathlib import Path

            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "data.bin"
                with open(path, "wb") as f:
                    f.write(bytes([0, 255, 128]))
                assert path.read_bytes() == bytes([0, 255, 128])
            ```

            ### Exclusive create with mode x

            ```python
            import tempfile
            from pathlib import Path

            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "new.txt"
                with open(path, "x", encoding="utf-8") as f:
                    f.write("created")
                try:
                    open(path, "x", encoding="utf-8")
                    created_twice = True
                except FileExistsError:
                    created_twice = False
                assert not created_twice
            ```

            ## Best practices

            - Always use `with open(...)` so files close even when exceptions occur.
            - Specify `encoding="utf-8"` for text files when portability matters.
            - Use `pathlib.Path.read_text` / `write_text` for small files when convenience beats fine-grained control.
            """
        ).strip(),
    },
    "ord": {
        "h1": "# [ord()](https://docs.python.org/3/library/functions.html#ord)",
        "short": "Returns the Unicode code point for a one-character string, or a byte value for length-1 bytes.",
        "body": textwrap.dedent(
            """
            ## Description

            `ord(character)` returns the integer Unicode code point for a one-character string, or the byte value for a length-1 `bytes`/`bytearray` object. It is the inverse of `chr()`.

            ## What problem it solves

            Character encoding work, validating ASCII, building translation tables, and converting between characters and numeric code points.

            ## Implementation options

            ### ASCII letters

            ```python
            assert ord("A") == 65
            assert ord("z") == 122
            assert chr(65) == "A"
            ```

            ### Single byte from bytes

            ```python
            assert ord(b"a") == 97
            ```

            ### Build a simple Caesar shift for lowercase letters

            ```python
            def shift(char, delta):
                base = ord("a")
                idx = (ord(char) - base + delta) % 26
                return chr(base + idx)

            assert shift("a", 3) == "d"
            assert shift("y", 3) == "b"
            ```

            ## Best practices

            - `ord()` requires exactly one character—multi-character strings raise `TypeError`.
            - For full Unicode handling beyond BMP, prefer str methods and the `unicodedata` module.
            - Pair `ord`/`chr` for teaching encodings; use `.encode()`/`.decode()` for real I/O.
            """
        ).strip(),
    },
    "pow": {
        "h1": "# [pow()](https://docs.python.org/3/library/functions.html#pow)",
        "short": "Raises base to exp, optionally modulo mod; supports efficient modular exponentiation.",
        "body": textwrap.dedent(
            """
            ## Description

            `pow(base, exp, mod=None)` returns `base` raised to `exp`. With three integer arguments, it computes modular exponentiation efficiently. Two-argument form matches the `**` operator.

            ## What problem it solves

            Exponentiation in math and cryptography—especially large powers modulo n, where the three-argument form avoids huge intermediate values.

            ## Implementation options

            ### Simple powers

            ```python
            assert pow(2, 10) == 1024
            assert pow(10, -2) == 0.01
            ```

            ### Modular exponentiation

            ```python
            assert pow(2, 100, 1000) == 376
            assert pow(38, -1, 97) == 23
            assert 23 * 38 % 97 == 1
            ```

            ### Equivalent to ** for two arguments

            ```python
            assert pow(3, 4) == 3 ** 4 == 81
            ```

            ## Best practices

            - Use three-argument `pow(base, exp, mod)` for crypto and large modular math—not `(base ** exp) % mod`.
            - Negative exponents with mod require base and mod to be relatively prime (see docs).
            - Watch float/complex rules: negative non-integer exponents on negatives yield complex results.
            """
        ).strip(),
    },
    "print": {
        "h1": "# [print()](https://docs.python.org/3/library/functions.html#print)",
        "short": "Writes objects as text to a stream, separated by sep and terminated with end.",
        "body": textwrap.dedent(
            """
            ## Description

            `print(*objects, sep=' ', end='\\n', file=None, flush=False)` converts objects to strings and writes them to `sys.stdout` by default. Keyword arguments control separators, line endings, output stream, and flushing.

            ## What problem it solves

            Quick user feedback, logging prototypes, and formatted console output without manual `sys.stdout.write` calls.

            ## Implementation options

            ### Default printing and custom separator

            ```python
            import io

            buf = io.StringIO()
            print("a", "b", "c", sep="-", file=buf)
            assert buf.getvalue() == "a-b-c\\n"
            ```

            ### Suppress trailing newline

            ```python
            import io

            buf = io.StringIO()
            print("loading", end="", file=buf)
            print(".", end="", file=buf)
            assert buf.getvalue() == "loading."
            ```

            ### Print to stderr for diagnostics

            ```python
            import io
            import sys

            err = io.StringIO()
            print("warning: low disk", file=err)
            assert "warning" in err.getvalue()
            ```

            ## Best practices

            - Use the `logging` module for production diagnostics; `print` for scripts and quick debugging.
            - Specify `file=` when testing print output with `io.StringIO`.
            - `print` converts with `str()`—implement `__str__` on custom types for readable output.
            """
        ).strip(),
    },
    "property": {
        "h1": "# [property()](https://docs.python.org/3/library/functions.html#property)",
        "short": "Defines managed attributes with getter, setter, deleter, and optional docstring.",
        "body": textwrap.dedent(
            """
            ## Description

            `property(fget=None, fset=None, fdel=None, doc=None)` returns a property descriptor. The `@property` decorator builds read-only or read-write attributes that run methods on access, assignment, or deletion.

            ## What problem it solves

            Encapsulation—validate on set, compute on get, deprecate direct attribute access—while keeping a clean `obj.attr` syntax.

            ## Implementation options

            ### Read-only computed attribute

            ```python
            class Circle:
                def __init__(self, radius):
                    self.radius = radius

                @property
                def area(self):
                    return 3.14159 * self.radius ** 2

            c = Circle(2)
            assert round(c.area, 4) == 12.5664
            ```

            ### Getter, setter, and validation

            ```python
            class Account:
                def __init__(self, balance):
                    self._balance = balance

                @property
                def balance(self):
                    return self._balance

                @balance.setter
                def balance(self, value):
                    if value < 0:
                        raise ValueError("balance cannot be negative")
                    self._balance = value

            acct = Account(100)
            acct.balance = 150
            assert acct.balance == 150
            ```

            ### Functional property() constructor form

            ```python
            class Temperature:
                def __init__(self, celsius):
                    self._celsius = celsius

                def get_c(self):
                    return self._celsius

                def set_c(self, value):
                    self._celsius = value

                celsius = property(get_c, set_c)

            t = Temperature(20)
            t.celsius = 25
            assert t.celsius == 25
            ```

            ## Best practices

            - Prefer `@property` decorator syntax over manual `property(get, set)` when methods already exist.
            - Keep property methods cheap—heavy work belongs in explicit methods.
            - Document managed attributes in the property docstring; it becomes the attribute's help text.
            """
        ).strip(),
    },
}


def extract_python_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    in_block = False
    current: list[str] = []
    for line in markdown.splitlines():
        if line.strip() == "```python":
            in_block = True
            current = []
            continue
        if in_block and line.strip() == "```":
            blocks.append("\n".join(current))
            in_block = False
            continue
        if in_block:
            current.append(line)
    return blocks


def validate_blocks() -> None:
    for slug, page in PAGES.items():
        for i, block in enumerate(extract_python_blocks(page["body"]), start=1):
            ns: dict = {}
            try:
                exec(block, ns, ns)
            except Exception as exc:  # noqa: BLE001
                raise RuntimeError(f"{slug} block {i} failed: {exc}\n{block}") from exc


def write_pages() -> None:
    descriptions: dict[str, str] = {}
    for slug, page in PAGES.items():
        path = DOCS / slug / "index.md"
        content = f"{page['h1']}\n\n{page['body']}\n"
        path.write_text(content, encoding="utf-8")
        descriptions[slug] = page["short"]
        line_count = len(content.splitlines())
        if line_count <= 20:
            raise RuntimeError(f"{slug} only has {line_count} lines after enrichment")

    json_path = ROOT / "scripts/builtin-fn-descriptions-part3.json"
    json_path.write_text(json.dumps(descriptions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    validate_blocks()
    write_pages()
    print(f"Enriched {len(PAGES)} functions")


if __name__ == "__main__":
    main()
