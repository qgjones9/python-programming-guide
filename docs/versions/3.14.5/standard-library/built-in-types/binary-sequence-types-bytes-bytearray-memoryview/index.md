# [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3/library/stdtypes.html/#binary-sequence-types-bytes-bytearray-memoryview)

Binary data in Python is handled by **`bytes`** (immutable) and **`bytearray`** (mutable)—sequences of integers in `0..255`. **`memoryview`** exposes another object's buffer without copying. Full specification remains on [docs.python.org](https://docs.python.org/3/library/stdtypes.html/#binary-sequence-types-bytes-bytearray-memoryview); this page explains how these types fit everyday I/O, networking, and parsing.

---

## Role of binary types in Python programs

**`bytes`** is the natural result of **`str.encode()`** and of reading files opened in binary mode. **`bytearray`** is useful when you must mutate a buffer in place (for example resizing or patching packet fields). **`memoryview`** lets C extensions, `struct`, and `array` share memory efficiently.

For typed numeric arrays (32-bit ints, doubles), see the [**`array`**](https://docs.python.org/3/library/array.html) module. Pair decoding with the [**Text Sequence Type — str**](../text-sequence-type-str/index.md) (`decode` / `encode`).

Both `bytes` and `bytearray` implement [**common sequence operations**](../sequence-types-list-tuple-range/common-sequence-operations/index.md). Indexing returns an **`int`**; slicing returns a **`bytes`** or **`bytearray`** object of length 1—unlike `str`, where `s[0]` and `s[0:1]` are both strings.

---

## [Bytes objects](https://docs.python.org/3/library/stdtypes.html/#bytes-objects)

**`bytes`** objects are **immutable** sequences of single bytes (`0 <= x < 256`). Many wire formats are ASCII-based, so several methods mirror `str` but only for ASCII-compatible data—avoid those on arbitrary binary payloads.

### Construction and literals

| Form | Example |
|------|--------|
| Literal (ASCII only) | `b'hello'`, `b"double quotes ok"`, `b'''triple'''` |
| Raw literal | `rb'\n'` disables escape processing |
| Zero-filled | `bytes(10)` |
| From ints | `bytes(range(256))` |
| Buffer copy | `bytes(existing_bytes_like)` |

Literal rules match [String and Bytes literals](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals) with a **`b`** prefix; only ASCII code points may appear literally—use escapes for values above 127.

Since 2 hexadecimal digits correspond precisely to a single byte, hexadecimal numbers are a commonly used format for describing binary data. Accordingly, the bytes type has an additional class method to read data in that format:

### `bytes.fromhex(string, /)`

This bytes class method returns a bytes object, decoding the given string object. The string must contain two hexadecimal digits per byte, with ASCII whitespace being ignored.

```python
bytes.fromhex('2Ef0 F1f2  ')
b'.\xf0\xf1\xf2'
```

> **Changed in version 3.7:** bytes.fromhex() now skips all ASCII whitespace in the string, not just spaces.

> **Changed in version 3.14:** bytes.fromhex() now accepts ASCII bytes and bytes-like objects as input.

A reverse conversion function exists to transform a bytes object into its hexadecimal representation.

### `bytes.hex(...)`

Return a string object containing two hexadecimal digits for each byte in the instance.

```python
b'\xf0\xf1\xf2'.hex()
'f0f1f2'
```

If you want to make the hex string easier to read, you can specify a single character separator sep parameter to include in the output. By default, this separator will be included between each byte. A second optional bytes_per_sep parameter controls the spacing. Positive values calculate the separator position from the right, negative values from the left.

```python
value = b'\xf0\xf1\xf2'
value.hex('-')
'f0-f1-f2'
value.hex('_', 2)
'f0_f1f2'
b'UUDDLRLRAB'.hex(' ', -4)
'55554444 4c524c52 4142'
```

> **Added in version 3.5.**

> **Changed in version 3.8:** bytes.hex() now supports optional sep and bytes_per_sep parameters to insert separators between bytes in the hex output.

Since bytes objects are sequences of integers (akin to a tuple), for a bytes object b, b[0] will be an integer, while b[0:1] will be a bytes object of length 1. (This contrasts with text strings, where both indexing and slicing will produce a string of length 1)

The representation of bytes objects uses the literal format (b'...') since it is often more useful than e.g. bytes([46, 46, 46]). You can always convert a bytes object into a list of integers using list(b).


---

## [Bytearray objects](https://docs.python.org/3/library/stdtypes.html/#bytearray-objects)

**`bytearray`** is the **mutable** counterpart to `bytes`. There is no literal syntax—always call the constructor. Mutable-sequence operations apply in addition to the shared bytes API below.

| Form | Example |
|------|--------|
| Empty | `bytearray()` |
| Zero-filled | `bytearray(10)` |
| From ints | `bytearray(range(20))` |
| Buffer copy | `bytearray(b'Hi!')` |

Since 2 hexadecimal digits correspond precisely to a single byte, hexadecimal numbers are a commonly used format for describing binary data. Accordingly, the bytearray type has an additional class method to read data in that format:

### `bytearray.fromhex(string, /)`

This bytearray class method returns bytearray object, decoding the given string object. The string must contain two hexadecimal digits per byte, with ASCII whitespace being ignored.

```python
bytearray.fromhex('2Ef0 F1f2  ')
bytearray(b'.\xf0\xf1\xf2')
```

> **Changed in version 3.7:** bytearray.fromhex() now skips all ASCII whitespace in the string, not just spaces.

> **Changed in version 3.14:** bytearray.fromhex() now accepts ASCII bytes and bytes-like objects as input.

A reverse conversion function exists to transform a bytearray object into its hexadecimal representation.

### `bytearray.hex(...)`

Return a string object containing two hexadecimal digits for each byte in the instance.

```python
bytearray(b'\xf0\xf1\xf2').hex()
'f0f1f2'
```

> **Added in version 3.5.**

> **Changed in version 3.8:** Similar to bytes.hex(), bytearray.hex() now supports optional sep and bytes_per_sep parameters to insert separators between bytes in the hex output.

### `bytearray.resize(size, /)`

Resize the bytearray to contain size bytes. size must be greater than or equal to 0.

If the bytearray needs to shrink, bytes beyond size are truncated.

If the bytearray needs to grow, all new bytes, those beyond size, will be set to null bytes.

This is equivalent to:

```python
def resize(ba, size):
    if len(ba) > size:
        del ba[size:]
    else:
        ba += b'\0' * (size - len(ba))
```

Examples:

```python
shrink = bytearray(b'abc')
shrink.resize(1)
(shrink, len(shrink))
(bytearray(b'a'), 1)
grow = bytearray(b'abc')
grow.resize(5)
(grow, len(grow))
(bytearray(b'abc\x00\x00'), 5)
```

> **Added in version 3.14.**

Since bytearray objects are sequences of integers (akin to a list), for a bytearray object b, b[0] will be an integer, while b[0:1] will be a bytearray object of length 1. (This contrasts with text strings, where both indexing and slicing will produce a string of length 1)

The representation of bytearray objects uses the bytes literal format (bytearray(b'...')) since it is often more useful than e.g. bytearray([46, 46, 46]). You can always convert a bytearray object into a list of integers using list(b).

**See also:** For detailed information on thread-safety guarantees for bytearray objects, see Thread safety for bytearray objects.


---

## [Bytes and bytearray methods (reference)](https://docs.python.org/3/library/stdtypes.html/#bytes-and-bytearray-operations)

Methods below are shared by **`bytes`** and **`bytearray`** unless noted. Operands may be any **bytes-like object**; return type may depend on operand order. Methods do **not** accept `str` arguments (use encoded bytes instead).

!!! note
    ASCII-oriented methods (`isalpha`, `lower`, `split` with default whitespace, etc.) assume ASCII-compatible data. On arbitrary binary, prefer the **binary-safe** group or pass explicit byte arguments.

| Method | Category | Typical use |
|--------|----------|-------------|
| [`bytes.count()` / `bytearray.count()`](#bytescount) | Search, test, and count | find where subsequences occur, test boundaries, or count matches |
| [`bytes.find()` / `bytearray.find()`](#bytesfind) | Search, test, and count | find where subsequences occur, test boundaries, or count matches |
| [`bytes.rfind()` / `bytearray.rfind()`](#bytesrfind) | Search, test, and count | find where subsequences occur, test boundaries, or count matches |
| [`bytes.index()` / `bytearray.index()`](#bytesindex) | Search, test, and count | find where subsequences occur, test boundaries, or count matches |
| [`bytes.rindex()` / `bytearray.rindex()`](#bytesrindex) | Search, test, and count | find where subsequences occur, test boundaries, or count matches |
| [`bytes.startswith()` / `bytearray.startswith()`](#bytesstartswith) | Search, test, and count | find where subsequences occur, test boundaries, or count matches |
| [`bytes.endswith()` / `bytearray.endswith()`](#bytesendswith) | Search, test, and count | find where subsequences occur, test boundaries, or count matches |
| [`bytes.split()` / `bytearray.split()`](#bytessplit) | Split, join, and partition | break binary data apart or concatenate bytes-like iterables |
| [`bytes.rsplit()` / `bytearray.rsplit()`](#bytesrsplit) | Split, join, and partition | break binary data apart or concatenate bytes-like iterables |
| [`bytes.splitlines()` / `bytearray.splitlines()`](#bytessplitlines) | Split, join, and partition | break binary data apart or concatenate bytes-like iterables |
| [`bytes.partition()` / `bytearray.partition()`](#bytespartition) | Split, join, and partition | break binary data apart or concatenate bytes-like iterables |
| [`bytes.rpartition()` / `bytearray.rpartition()`](#bytesrpartition) | Split, join, and partition | break binary data apart or concatenate bytes-like iterables |
| [`bytes.join()` / `bytearray.join()`](#bytesjoin) | Split, join, and partition | break binary data apart or concatenate bytes-like iterables |
| [`bytes.strip()` / `bytearray.strip()`](#bytesstrip) | Strip, prefix, and suffix | trim edges or remove/add fixed byte affixes |
| [`bytes.lstrip()` / `bytearray.lstrip()`](#byteslstrip) | Strip, prefix, and suffix | trim edges or remove/add fixed byte affixes |
| [`bytes.rstrip()` / `bytearray.rstrip()`](#bytesrstrip) | Strip, prefix, and suffix | trim edges or remove/add fixed byte affixes |
| [`bytes.removeprefix()` / `bytearray.removeprefix()`](#bytesremoveprefix) | Strip, prefix, and suffix | trim edges or remove/add fixed byte affixes |
| [`bytes.removesuffix()` / `bytearray.removesuffix()`](#bytesremovesuffix) | Strip, prefix, and suffix | trim edges or remove/add fixed byte affixes |
| [`bytes.center()` / `bytearray.center()`](#bytescenter) | Padding and alignment | pad or align binary data in a fixed-width field |
| [`bytes.ljust()` / `bytearray.ljust()`](#bytesljust) | Padding and alignment | pad or align binary data in a fixed-width field |
| [`bytes.rjust()` / `bytearray.rjust()`](#bytesrjust) | Padding and alignment | pad or align binary data in a fixed-width field |
| [`bytes.zfill()` / `bytearray.zfill()`](#byteszfill) | Padding and alignment | pad or align binary data in a fixed-width field |
| [`bytes.expandtabs()` / `bytearray.expandtabs()`](#bytesexpandtabs) | Padding and alignment | pad or align binary data in a fixed-width field |
| [`bytes.replace()` / `bytearray.replace()`](#bytesreplace) | Transform and decode | replace content, translate bytes, or decode to `str` |
| [`bytes.translate()` / `bytearray.translate()`](#bytestranslate) | Transform and decode | replace content, translate bytes, or decode to `str` |
| [`bytes.maketrans()` / `bytearray.maketrans()`](#bytesmaketrans) | Transform and decode | replace content, translate bytes, or decode to `str` |
| [`bytes.decode()` / `bytearray.decode()`](#bytesdecode) | Transform and decode | replace content, translate bytes, or decode to `str` |
| [`bytes.capitalize()` / `bytearray.capitalize()`](#bytescapitalize) | Case and title (ASCII) | change ASCII letter case for display or comparisons |
| [`bytes.lower()` / `bytearray.lower()`](#byteslower) | Case and title (ASCII) | change ASCII letter case for display or comparisons |
| [`bytes.upper()` / `bytearray.upper()`](#bytesupper) | Case and title (ASCII) | change ASCII letter case for display or comparisons |
| [`bytes.swapcase()` / `bytearray.swapcase()`](#bytesswapcase) | Case and title (ASCII) | change ASCII letter case for display or comparisons |
| [`bytes.title()` / `bytearray.title()`](#bytestitle) | Case and title (ASCII) | change ASCII letter case for display or comparisons |
| [`bytes.isalnum()` / `bytearray.isalnum()`](#bytesisalnum) | Classification (`is*` methods, ASCII) | test ASCII character categories |
| [`bytes.isalpha()` / `bytearray.isalpha()`](#bytesisalpha) | Classification (`is*` methods, ASCII) | test ASCII character categories |
| [`bytes.isascii()` / `bytearray.isascii()`](#bytesisascii) | Classification (`is*` methods, ASCII) | test ASCII character categories |
| [`bytes.isdigit()` / `bytearray.isdigit()`](#bytesisdigit) | Classification (`is*` methods, ASCII) | test ASCII character categories |
| [`bytes.islower()` / `bytearray.islower()`](#bytesislower) | Classification (`is*` methods, ASCII) | test ASCII character categories |
| [`bytes.isspace()` / `bytearray.isspace()`](#bytesisspace) | Classification (`is*` methods, ASCII) | test ASCII character categories |
| [`bytes.istitle()` / `bytearray.istitle()`](#bytesistitle) | Classification (`is*` methods, ASCII) | test ASCII character categories |
| [`bytes.isupper()` / `bytearray.isupper()`](#bytesisupper) | Classification (`is*` methods, ASCII) | test ASCII character categories |

---

### Search, test, and count

Methods in this group find where subsequences occur, test boundaries, or count matches. Each returns a **new** `bytes` or `bytearray` (or `str` / `bool` / `list`) unless noted; **`bytearray` methods never mutate in place**.

<a id="bytescount"></a>

### `bytes.count(sub[, start[, end]])`

Return the number of non-overlapping occurrences of subsequence sub in the range [start, end]. Optional arguments start and end are interpreted as in slice notation.

The subsequence to search for may be any bytes-like object or an integer in the range 0 to 255.

If sub is empty, returns the number of empty slices between characters which is the length of the bytes object plus one.

> **Changed in version 3.3:** Also accept an integer in the range 0 to 255 as the subsequence.

<a id="bytesfind"></a>

### `bytes.find(sub[, start[, end]])`

Return the lowest index in the data where the subsequence sub is found, such that sub is contained in the slice s[start:end]. Optional arguments start and end are interpreted as in slice notation. Return -1 if sub is not found.

The subsequence to search for may be any bytes-like object or an integer in the range 0 to 255.

!!! note
    The find() method should be used only if you need to know the position of sub. To check if sub is a substring or not, use the in operator:

```python
b'Py' in b'Python'
True
```

> **Changed in version 3.3:** Also accept an integer in the range 0 to 255 as the subsequence.

<a id="bytesrfind"></a>

### `bytes.rfind(sub[, start[, end]])`

Return the highest index in the sequence where the subsequence sub is found, such that sub is contained within s[start:end]. Optional arguments start and end are interpreted as in slice notation. Return -1 on failure.

The subsequence to search for may be any bytes-like object or an integer in the range 0 to 255.

> **Changed in version 3.3:** Also accept an integer in the range 0 to 255 as the subsequence.

<a id="bytesindex"></a>

### `bytes.index(sub[, start[, end]])`

Like find(), but raise ValueError when the subsequence is not found.

The subsequence to search for may be any bytes-like object or an integer in the range 0 to 255.

> **Changed in version 3.3:** Also accept an integer in the range 0 to 255 as the subsequence.

<a id="bytesrindex"></a>

### `bytes.rindex(sub[, start[, end]])`

Like rfind() but raises ValueError when the subsequence sub is not found.

The subsequence to search for may be any bytes-like object or an integer in the range 0 to 255.

> **Changed in version 3.3:** Also accept an integer in the range 0 to 255 as the subsequence.

<a id="bytesstartswith"></a>

### `bytes.startswith(prefix[, start[, end]])`

Return True if the binary data starts with the specified prefix, otherwise return False. prefix can also be a tuple of prefixes to look for. With optional start, test beginning at that position. With optional end, stop comparing at that position.

The prefix(es) to search for may be any bytes-like object.

<a id="bytesendswith"></a>

### `bytes.endswith(suffix[, start[, end]])`

Return True if the binary data ends with the specified suffix, otherwise return False. suffix can also be a tuple of suffixes to look for. With optional start, test beginning at that position. With optional end, stop comparing at that position.

The suffix(es) to search for may be any bytes-like object.

---

### Split, join, and partition

Methods in this group break binary data apart or concatenate bytes-like iterables. Each returns a **new** `bytes` or `bytearray` (or `str` / `bool` / `list`) unless noted; **`bytearray` methods never mutate in place**.

<a id="bytessplit"></a>

### `bytes.split(sep=None, maxsplit=-1)`

Split the binary sequence into subsequences of the same type, using sep as the delimiter string. If maxsplit is given and non-negative, at most maxsplit splits are done (thus, the list will have at most maxsplit+1 elements). If maxsplit is not specified or is -1, then there is no limit on the number of splits (all possible splits are made).

If sep is given, consecutive delimiters are not grouped together and are deemed to delimit empty subsequences (for example, b'1,,2'.split(b',') returns [b'1', b'', b'2']). The sep argument may consist of a multibyte sequence as a single delimiter. Splitting an empty sequence with a specified separator returns [b''] or [bytearray(b'')] depending on the type of object being split. The sep argument may be any bytes-like object.

For example:

```python
b'1,2,3'.split(b',')
[b'1', b'2', b'3']
b'1,2,3'.split(b',', maxsplit=1)
[b'1', b'2,3']
b'1,2,,3,'.split(b',')
[b'1', b'2', b'', b'3', b'']
b'1<>2<>3<4'.split(b'<>')
[b'1', b'2', b'3<4']
```

If sep is not specified or is None, a different splitting algorithm is applied: runs of consecutive ASCII whitespace are regarded as a single separator, and the result will contain no empty strings at the start or end if the sequence has leading or trailing whitespace. Consequently, splitting an empty sequence or a sequence consisting solely of ASCII whitespace without a specified separator returns [].

For example:

```python
b'1 2 3'.split()
[b'1', b'2', b'3']
b'1 2 3'.split(maxsplit=1)
[b'1', b'2 3']
b'   1   2   3   '.split()
[b'1', b'2', b'3']
```

<a id="bytesrsplit"></a>

### `bytes.rsplit(sep=None, maxsplit=-1)`

Split the binary sequence into subsequences of the same type, using sep as the delimiter string. If maxsplit is given, at most maxsplit splits are done, the rightmost ones. If sep is not specified or None, any subsequence consisting solely of ASCII whitespace is a separator. Except for splitting from the right, rsplit() behaves like split() which is described in detail below.

<a id="bytessplitlines"></a>

### `bytes.splitlines(keepends=False)`

Return a list of the lines in the binary sequence, breaking at ASCII line boundaries. This method uses the universal newlines approach to splitting lines. Line breaks are not included in the resulting list unless keepends is given and true.

For example:

```python
b'ab c\n\nde fg\rkl\r\n'.splitlines()
[b'ab c', b'', b'de fg', b'kl']
b'ab c\n\nde fg\rkl\r\n'.splitlines(keepends=True)
[b'ab c\n', b'\n', b'de fg\r', b'kl\r\n']
```

Unlike split() when a delimiter string sep is given, this method returns an empty list for the empty string, and a terminal line break does not result in an extra line:

```python
b"".split(b'\n'), b"Two lines\n".split(b'\n')
([b''], [b'Two lines', b''])
b"".splitlines(), b"One line\n".splitlines()
([], [b'One line'])
```

<a id="bytespartition"></a>

### `bytes.partition(sep, /)`

Split the sequence at the first occurrence of sep, and return a 3-tuple containing the part before the separator, the separator itself or its bytearray copy, and the part after the separator. If the separator is not found, return a 3-tuple containing a copy of the original sequence, followed by two empty bytes or bytearray objects.

The separator to search for may be any bytes-like object.

<a id="bytesrpartition"></a>

### `bytes.rpartition(sep, /)`

Split the sequence at the last occurrence of sep, and return a 3-tuple containing the part before the separator, the separator itself or its bytearray copy, and the part after the separator. If the separator is not found, return a 3-tuple containing two empty bytes or bytearray objects, followed by a copy of the original sequence.

The separator to search for may be any bytes-like object.

<a id="bytesjoin"></a>

### `bytes.join(iterable, /)`

Return a bytes or bytearray object which is the concatenation of the binary data sequences in iterable. A TypeError will be raised if there are any values in iterable that are not bytes-like objects, including str objects. The separator between elements is the contents of the bytes or bytearray object providing this method.

---

### Strip, prefix, and suffix

Methods in this group trim edges or remove/add fixed byte affixes. Each returns a **new** `bytes` or `bytearray` (or `str` / `bool` / `list`) unless noted; **`bytearray` methods never mutate in place**.

<a id="bytesstrip"></a>

### `bytes.strip(bytes=None, /)`

Return a copy of the sequence with specified leading and trailing bytes removed. The bytes argument is a binary sequence specifying the set of byte values to be removed. If omitted or None, the bytes argument defaults to removing ASCII whitespace. The bytes argument is not a prefix or suffix; rather, all combinations of its values are stripped:

```python
b'   spacious   '.strip()
b'spacious'
b'www.example.com'.strip(b'cmowz.')
b'example'
```

The binary sequence of byte values to remove may be any bytes-like object.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

The following methods on bytes and bytearray objects assume the use of ASCII compatible binary formats and should not be applied to arbitrary binary data. Note that all of the bytearray methods in this section do not operate in place, and instead produce new objects.

<a id="byteslstrip"></a>

### `bytes.lstrip(bytes=None, /)`

Return a copy of the sequence with specified leading bytes removed. The bytes argument is a binary sequence specifying the set of byte values to be removed. If omitted or None, the bytes argument defaults to removing ASCII whitespace. The bytes argument is not a prefix; rather, all combinations of its values are stripped:

```python
b'   spacious   '.lstrip()
b'spacious   '
b'www.example.com'.lstrip(b'cmowz.')
b'example.com'
```

The binary sequence of byte values to remove may be any bytes-like object. See removeprefix() for a method that will remove a single prefix string rather than all of a set of characters. For example:

```python
b'Arthur: three!'.lstrip(b'Arthur: ')
b'ee!'
b'Arthur: three!'.removeprefix(b'Arthur: ')
b'three!'
```

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytesrstrip"></a>

### `bytes.rstrip(bytes=None, /)`

Return a copy of the sequence with specified trailing bytes removed. The bytes argument is a binary sequence specifying the set of byte values to be removed. If omitted or None, the bytes argument defaults to removing ASCII whitespace. The bytes argument is not a suffix; rather, all combinations of its values are stripped:

```python
b'   spacious   '.rstrip()
b'   spacious'
b'mississippi'.rstrip(b'ipz')
b'mississ'
```

The binary sequence of byte values to remove may be any bytes-like object. See removesuffix() for a method that will remove a single suffix string rather than all of a set of characters. For example:

```python
b'Monty Python'.rstrip(b' Python')
b'M'
b'Monty Python'.removesuffix(b' Python')
b'Monty'
```

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytesremoveprefix"></a>

### `bytes.removeprefix(prefix, /)`

If the binary data starts with the prefix string, return bytes[len(prefix):]. Otherwise, return a copy of the original binary data:

```python
b'TestHook'.removeprefix(b'Test')
b'Hook'
b'BaseTestCase'.removeprefix(b'Test')
b'BaseTestCase'
```

The prefix may be any bytes-like object.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

> **Added in version 3.9.**

<a id="bytesremovesuffix"></a>

### `bytes.removesuffix(suffix, /)`

If the binary data ends with the suffix string and that suffix is not empty, return bytes[:-len(suffix)]. Otherwise, return a copy of the original binary data:

```python
b'MiscTests'.removesuffix(b'Tests')
b'Misc'
b'TmpDirMixin'.removesuffix(b'Tests')
b'TmpDirMixin'
```

The suffix may be any bytes-like object.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

> **Added in version 3.9.**

---

### Padding and alignment

Methods in this group pad or align binary data in a fixed-width field. Each returns a **new** `bytes` or `bytearray` (or `str` / `bool` / `list`) unless noted; **`bytearray` methods never mutate in place**.

<a id="bytescenter"></a>

### `bytes.center(width, fillbyte=b' ', /)`

Return a copy of the object centered in a sequence of length width. Padding is done using the specified fillbyte (default is an ASCII space). For bytes objects, the original sequence is returned if width is less than or equal to len(s).

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytesljust"></a>

### `bytes.ljust(width, fillbyte=b' ', /)`

Return a copy of the object left justified in a sequence of length width. Padding is done using the specified fillbyte (default is an ASCII space). For bytes objects, the original sequence is returned if width is less than or equal to len(s).

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytesrjust"></a>

### `bytes.rjust(width, fillbyte=b' ', /)`

Return a copy of the object right justified in a sequence of length width. Padding is done using the specified fillbyte (default is an ASCII space). For bytes objects, the original sequence is returned if width is less than or equal to len(s).

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="byteszfill"></a>

### `bytes.zfill(width, /)`

Return a copy of the sequence left filled with ASCII b'0' digits to make a sequence of length width. A leading sign prefix (b'+'/ b'-') is handled by inserting the padding after the sign character rather than before. For bytes objects, the original sequence is returned if width is less than or equal to len(seq).

For example:

```python
b"42".zfill(5)
b'00042'
b"-42".zfill(5)
b'-0042'
```

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytesexpandtabs"></a>

### `bytes.expandtabs(tabsize=8)`

Return a copy of the sequence where all ASCII tab characters are replaced by one or more ASCII spaces, depending on the current column and the given tab size. Tab positions occur every tabsize bytes (default is 8, giving tab positions at columns 0, 8, 16 and so on). To expand the sequence, the current column is set to zero and the sequence is examined byte by byte. If the byte is an ASCII tab character (b'\t'), one or more space characters are inserted in the result until the current column is equal to the next tab position. (The tab character itself is not copied.) If the current byte is an ASCII newline (b'\n') or carriage return (b'\r'), it is copied and the current column is reset to zero. Any other byte value is copied unchanged and the current column is incremented by one regardless of how the byte value is represented when printed:

```python
b'01\t012\t0123\t01234'.expandtabs()
b'01      012     0123    01234'
b'01\t012\t0123\t01234'.expandtabs(4)
b'01  012 0123    01234'
```

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

---

### Transform and decode

Methods in this group replace content, translate bytes, or decode to `str`. Each returns a **new** `bytes` or `bytearray` (or `str` / `bool` / `list`) unless noted; **`bytearray` methods never mutate in place**.

<a id="bytesreplace"></a>

### `bytes.replace(old, new, count=-1, /)`

Return a copy of the sequence with all occurrences of subsequence old replaced by new. If the optional argument count is given, only the first count occurrences are replaced.

The subsequence to search for and its replacement may be any bytes-like object.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytestranslate"></a>

### `bytes.translate(table, /, delete=b'')`

Return a copy of the bytes or bytearray object where all bytes occurring in the optional argument delete are removed, and the remaining bytes have been mapped through the given translation table, which must be a bytes object of length 256.

You can use the bytes.maketrans() method to create a translation table.

Set the table argument to None for translations that only delete characters:

```python
b'read this short text'.translate(None, b'aeiou')
b'rd ths shrt txt'
```

> **Changed in version 3.6:** delete is now supported as a keyword argument.

The following methods on bytes and bytearray objects have default behaviours that assume the use of ASCII compatible binary formats, but can still be used with arbitrary binary data by passing appropriate arguments. Note that all of the bytearray methods in this section do not operate in place, and instead produce new objects.

<a id="bytesmaketrans"></a>

### `bytes.maketrans(from, to, /)`

static bytearray.maketrans(from, to, /)

This static method returns a translation table usable for bytes.translate() that will map each character in from into the character at the same position in to; from and to must both be bytes-like objects and have the same length.

> **Added in version 3.1.**

<a id="bytesdecode"></a>

### `bytes.decode(encoding='utf-8', errors='strict')`

Return the bytes decoded to a str.

encoding defaults to 'utf-8'; see Standard Encodings for possible values.

errors controls how decoding errors are handled. If 'strict' (the default), a UnicodeError exception is raised. Other possible values are 'ignore', 'replace', and any other name registered via codecs.register_error(). See Error Handlers for details.

For performance reasons, the value of errors is not checked for validity unless a decoding error actually occurs, Python Development Mode is enabled or a debug build is used.

!!! note
    Passing the encoding argument to str allows decoding any bytes-like object directly, without needing to make a temporary bytes or bytearray object.

> **Changed in version 3.1:** Added support for keyword arguments.

> **Changed in version 3.9:** The value of the errors argument is now checked in Python Development Mode and in debug mode.

---

### Case and title (ASCII)

Methods in this group change ASCII letter case for display or comparisons. Each returns a **new** `bytes` or `bytearray` (or `str` / `bool` / `list`) unless noted; **`bytearray` methods never mutate in place**.

<a id="bytescapitalize"></a>

### `bytes.capitalize()`

Return a copy of the sequence with each byte interpreted as an ASCII character, and the first byte capitalized and the rest lowercased. Non-ASCII byte values are passed through unchanged.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="byteslower"></a>

### `bytes.lower()`

Return a copy of the sequence with all the uppercase ASCII characters converted to their corresponding lowercase counterpart.

For example:

```python
b'Hello World'.lower()
b'hello world'
```

Lowercase ASCII characters are those byte values in the sequence b'abcdefghijklmnopqrstuvwxyz'. Uppercase ASCII characters are those byte values in the sequence b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytesupper"></a>

### `bytes.upper()`

Return a copy of the sequence with all the lowercase ASCII characters converted to their corresponding uppercase counterpart.

For example:

```python
b'Hello World'.upper()
b'HELLO WORLD'
```

Lowercase ASCII characters are those byte values in the sequence b'abcdefghijklmnopqrstuvwxyz'. Uppercase ASCII characters are those byte values in the sequence b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytesswapcase"></a>

### `bytes.swapcase()`

Return a copy of the sequence with all the lowercase ASCII characters converted to their corresponding uppercase counterpart and vice-versa.

For example:

```python
b'Hello World'.swapcase()
b'hELLO wORLD'
```

Lowercase ASCII characters are those byte values in the sequence b'abcdefghijklmnopqrstuvwxyz'. Uppercase ASCII characters are those byte values in the sequence b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.

Unlike str.swapcase(), it is always the case that bin.swapcase().swapcase() == bin for the binary versions. Case conversions are symmetrical in ASCII, even though that is not generally true for arbitrary Unicode code points.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

<a id="bytestitle"></a>

### `bytes.title()`

Return a titlecased version of the binary sequence where words start with an uppercase ASCII character and the remaining characters are lowercase. Uncased byte values are left unmodified.

For example:

```python
b'Hello world'.title()
b'Hello World'
```

Lowercase ASCII characters are those byte values in the sequence b'abcdefghijklmnopqrstuvwxyz'. Uppercase ASCII characters are those byte values in the sequence b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'. All other byte values are uncased.

The algorithm uses a simple language-independent definition of a word as groups of consecutive letters. The definition works in many contexts but it means that apostrophes in contractions and possessives form word boundaries, which may not be the desired result:

```python
b"they're bill's friends from the UK".title()
b"They'Re Bill'S Friends From The Uk"
A workaround for apostrophes can be constructed using regular expressions:
```

```python
import re
def titlecase(s):
    return re.sub(rb"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0:1].upper() +
                             mo.group(0)[1:].lower(),
                  s)
```

```python
titlecase(b"they're bill's friends.")
b"They're Bill's Friends."
```

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

---

### Classification (`is*` methods, ASCII)

Methods in this group test ASCII character categories. Each returns a **new** `bytes` or `bytearray` (or `str` / `bool` / `list`) unless noted; **`bytearray` methods never mutate in place**.

<a id="bytesisalnum"></a>

### `bytes.isalnum()`

Return True if all bytes in the sequence are alphabetical ASCII characters or ASCII decimal digits and the sequence is not empty, False otherwise. Alphabetic ASCII characters are those byte values in the sequence b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'. ASCII decimal digits are those byte values in the sequence b'0123456789'.

For example:

```python
b'ABCabc1'.isalnum()
True
b'ABC abc1'.isalnum()
False
```

<a id="bytesisalpha"></a>

### `bytes.isalpha()`

Return True if all bytes in the sequence are alphabetic ASCII characters and the sequence is not empty, False otherwise. Alphabetic ASCII characters are those byte values in the sequence b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.

For example:

```python
b'ABCabc'.isalpha()
True
b'ABCabc1'.isalpha()
False
```

<a id="bytesisascii"></a>

### `bytes.isascii()`

Return True if the sequence is empty or all bytes in the sequence are ASCII, False otherwise. ASCII bytes are in the range 0-0x7F.

> **Added in version 3.7.**

<a id="bytesisdigit"></a>

### `bytes.isdigit()`

Return True if all bytes in the sequence are ASCII decimal digits and the sequence is not empty, False otherwise. ASCII decimal digits are those byte values in the sequence b'0123456789'.

For example:

```python
b'1234'.isdigit()
True
b'1.23'.isdigit()
False
```

<a id="bytesislower"></a>

### `bytes.islower()`

Return True if there is at least one lowercase ASCII character in the sequence and no uppercase ASCII characters, False otherwise.

For example:

```python
b'hello world'.islower()
True
b'Hello world'.islower()
False
```

Lowercase ASCII characters are those byte values in the sequence b'abcdefghijklmnopqrstuvwxyz'. Uppercase ASCII characters are those byte values in the sequence b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.

<a id="bytesisspace"></a>

### `bytes.isspace()`

Return True if all bytes in the sequence are ASCII whitespace and the sequence is not empty, False otherwise. ASCII whitespace characters are those byte values in the sequence b' \t\n\r\x0b\f' (space, tab, newline, carriage return, vertical tab, form feed).

<a id="bytesistitle"></a>

### `bytes.istitle()`

Return True if the sequence is ASCII titlecase and the sequence is not empty, False otherwise. See bytes.title() for more details on the definition of “titlecase”.

For example:

```python
b'Hello World'.istitle()
True
b'Hello world'.istitle()
False
```

<a id="bytesisupper"></a>

### `bytes.isupper()`

Return True if there is at least one uppercase alphabetic ASCII character in the sequence and no lowercase ASCII characters, False otherwise.

For example:

```python
b'HELLO WORLD'.isupper()
True
b'Hello world'.isupper()
False
```

Lowercase ASCII characters are those byte values in the sequence b'abcdefghijklmnopqrstuvwxyz'. Uppercase ASCII characters are those byte values in the sequence b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.

---

## [printf-style bytes formatting](https://docs.python.org/3/library/stdtypes.html/#printf-style-bytes-formatting)

!!! note
    These operations have historical quirks (e.g. failing to display tuples and dicts). Prefer **`bytes.join()`**, f-strings on `str`, or explicit struct packing for new code.

The **`%`** operator on **`bytes`** / **`bytearray`** performs **printf-style interpolation**: `format % values` replaces conversion specifications in `format`, similar to C `sprintf`.

- **Single argument:** `values` may be a non-tuple when the format expects one conversion.
- **Multiple arguments:** `values` must be a **tuple** of the right length, or a **mapping** for `%(name)s` keys (no `*` width/precision from a mapping).

When the right argument is a dictionary (or other mapping type), then the formats in the bytes object must include a parenthesised mapping key into that dictionary inserted immediately after the '%' character. The mapping key selects the value to be formatted from the mapping. For example:

```python
print(b'%(language)s has %(number)03d quote types.' %
      {b'language': b"Python", b"number": 2})
b'Python has 002 quote types.'
```

In this case no * specifiers may occur in a format (since they require a sequential parameter list).

The conversion flag characters are:


| Flag | Meaning |
|------|---------|
| `#` | “Alternate form” for the conversion (see notes below). |
| `0` | Zero-pad numeric values. |
| `-` | Left-adjust the converted value (overrides `0` if both are given). |
| ` ` (space) | Leave a blank before a positive number from a signed conversion. |
| `+` | Always show a sign (`+` or `-`); overrides the space flag. |

A length modifier (`h`, `l`, or `L`) may appear but is **ignored** in Python (`%ld` behaves like `%d`).

The conversion types are:


| Conversion | Meaning | Notes |
|------------|---------|-------|
| `d` | Signed integer decimal. | |
| `i` | Signed integer decimal. | |
| `o` | Signed octal. | (1) alternate: leading `0o`. |
| `u` | Obsolete; same as `d`. | (8) |
| `x` | Signed hex (lowercase). | (2) alternate: `0x`. |
| `X` | Signed hex (uppercase). | (2) alternate: `0X`. |
| `e` | Float, exponential (lowercase). | (3) |
| `E` | Float, exponential (uppercase). | (3) |
| `f` | Float, decimal format. | (3) |
| `F` | Float, decimal format. | (3) |
| `g` | Float; uses `%e` or `%f` style by magnitude. | (4) |
| `G` | Like `g` but uppercase exponent. | (4) |
| `c` | Single byte (int or single-byte object). | |
| `b` | Bytes (buffer protocol or `__bytes__()`). | (5) |
| `s` | Alias for `b` (legacy Python 2/3). | (6) deprecated |
| `a` | Bytes via `repr(obj).encode('ascii', 'backslashreplace')`. | (5) |
| `r` | Alias for `a` (legacy Python 2/3). | (7) deprecated |
| `%` | Literal `%` in the result. | |

**Notes:** (1) octal alternate form; (2) hex alternate `0x`/`0X`; (3) precision defaults to 6 fractional digits; (4) `%g`/`%G` significant digits; (5) buffer/`__bytes__`; (6)(7) deprecated aliases; (8) `%u` obsolete. See [PEP 461](https://peps.python.org/pep-0461/) and [PEP 237](https://peps.python.org/pep-0237/).

Signed integer decimal.

```python
'i'
Signed integer decimal.
'o'
Signed octal value.
(1)
'u'
Obsolete type – it is identical to 'd'.
(8)
'x'
Signed hexadecimal (lowercase).
(2)
'X'
Signed hexadecimal (uppercase).
(2)
'e'
Floating-point exponential format (lowercase).
(3)
'E'
Floating-point exponential format (uppercase).
(3)
'f'
Floating-point decimal format.
(3)
'F'
Floating-point decimal format.
(3)
'g'
Floating-point format. Uses lowercase exponential format if exponent is less than -4 or not less than precision, decimal format otherwise.
(4)
'G'
Floating-point format. Uses uppercase exponential format if exponent is less than -4 or not less than precision, decimal format otherwise.
(4)
'c'
Single byte (accepts integer or single byte objects).
'b'
```

Bytes (any object that follows the buffer protocol or has __bytes__()).

```python
(5)
's'
's' is an alias for 'b' and should only be used for Python2/3 code bases.
(6)
'a'
```

Bytes (converts any Python object using repr(obj).encode('ascii', 'backslashreplace')).

```python
(5)
'r'
'r' is an alias for 'a' and should only be used for Python2/3 code bases.
(7)
'%'
No argument is converted, results in a '%' character in the result.
Notes:
```

The alternate form causes a leading octal specifier ('0o') to be inserted before the first digit.

The alternate form causes a leading '0x' or '0X' (depending on whether the 'x' or 'X' format was used) to be inserted before the first digit.

The alternate form causes the result to always contain a decimal point, even if no digits follow it.

The precision determines the number of digits after the decimal point and defaults to 6.

The alternate form causes the result to always contain a decimal point, and trailing zeroes are not removed as they would otherwise be.

The precision determines the number of significant digits before and after the decimal point and defaults to 6.

If precision is N, the output is truncated to N characters.

```python
b'%s' is deprecated, but will not be removed during the 3.x series.
b'%r' is deprecated, but will not be removed during the 3.x series.
```

See PEP 237.

!!! note
    The bytearray version of this method does not operate in place - it always produces a new object, even if no changes were made.

**See also:** PEP 461 - Adding % formatting to bytes and bytearray

> **Added in version 3.5.**


> **Added in version 3.5:** See [PEP 461 — Adding % formatting to bytes and bytearray](https://peps.python.org/pep-0461/).

---

## [memoryview](https://docs.python.org/3/library/stdtypes.html/#memory-views)

**`memoryview`** references another object's **buffer protocol** memory **without copying**. Built-in exporters include `bytes`, `bytearray`, and `array.array`. An **element** is the atomic unit (often one byte).

### `memoryview(object)`

Create a memoryview referencing a **buffer protocol** object. **`memoryview`** is a **generic type** (3.14+) over the underlying element type.

A memoryview has the notion of an element, which is the atomic memory unit handled by the originating object. For many simple types such as bytes and bytearray, an element is a single byte, but other types such as array.array may have bigger elements.

memoryviews are generic over the type of their underlying data.

len(view) is equal to the length of tolist, which is the nested list representation of the view. If view.ndim = 1, this is equal to the number of elements in the view.

> **Changed in version 3.12:** If view.ndim == 0, len(view) now raises TypeError instead of returning 1.

The itemsize attribute will give you the number of bytes in a single element.

A memoryview supports slicing and indexing to expose its data. One-dimensional slicing will result in a subview:

```python
v = memoryview(b'abcefg')
v[1]
98
v[-1]
103
v[1:4]
<memory at 0x7f3ddc9f4350>
bytes(v[1:4])
b'bce'
```

If format is one of the native format specifiers from the struct module, indexing with an integer or a tuple of integers is also supported and returns a single element with the correct type. One-dimensional memoryviews can be indexed with an integer or a one-integer tuple. Multi-dimensional memoryviews can be indexed with tuples of exactly ndim integers where ndim is the number of dimensions. Zero-dimensional memoryviews can be indexed with the empty tuple.

Here is an example with a non-byte format:

```python
import array
a = array.array('l', [-11111111, 22222222, -33333333, 44444444])
m = memoryview(a)
m[0]
-11111111
m[-1]
44444444
m[::2].tolist()
[-11111111, -33333333]
```

If the underlying object is writable, the memoryview supports one-dimensional slice assignment. Resizing is not allowed:

```python
data = bytearray(b'abcefg')
v = memoryview(data)
v.readonly
False
v[0] = ord(b'z')
data
bytearray(b'zbcefg')
v[1:4] = b'123'
data
bytearray(b'z123fg')
v[2:3] = b'spam'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: memoryview assignment: lvalue and rvalue have different structures
v[2:6] = b'spam'
data
bytearray(b'z1spam')
```

One-dimensional memoryviews of hashable (read-only) types with formats ‘B’, ‘b’ or ‘c’ are also hashable. The hash is defined as hash(m) == hash(m.tobytes()):

```python
v = memoryview(b'abcefg')
hash(v) == hash(b'abcefg')
True
hash(v[2:4]) == hash(b'ce')
True
hash(v[::-2]) == hash(b'abcefg'[::-2])
True
```

> **Changed in version 3.3:** One-dimensional memoryviews can now be sliced. One-dimensional memoryviews with formats ‘B’, ‘b’ or ‘c’ are now hashable.

> **Changed in version 3.4:** memoryview is now registered automatically with collections.abc.Sequence

> **Changed in version 3.5:** memoryviews can now be indexed with tuple of integers.

> **Changed in version 3.14:** memoryview is now a generic type.


### Methods

<a id="memoryview__eq__"></a>

### `memoryview.__eq__(exporter)`

A memoryview and a PEP 3118 exporter are equal if their shapes are equivalent and if all corresponding values are equal when the operands’ respective format codes are interpreted using struct syntax.

For the subset of struct format strings currently supported by tolist(), v and w are equal if v.tolist() == w.tolist():

```python
import array
a = array.array('I', [1, 2, 3, 4, 5])
b = array.array('d', [1.0, 2.0, 3.0, 4.0, 5.0])
c = array.array('b', [5, 3, 1])
x = memoryview(a)
y = memoryview(b)
x == a == y == b
True
x.tolist() == a.tolist() == y.tolist() == b.tolist()
True
z = y[::-2]
z == c
True
z.tolist() == c.tolist()
True
```

If either format string is not supported by the struct module, then the objects will always compare as unequal (even if the format strings and buffer contents are identical):

```python
from ctypes import BigEndianStructure, c_long
class BEPoint(BigEndianStructure):
    _fields_ = [("x", c_long), ("y", c_long)]
point = BEPoint(100, 200)
a = memoryview(point)
b = memoryview(point)
a == point
False
a == b
False
```

!!! note
    that, as with floating-point numbers, v is w does not imply v == w for memoryview objects.

> **Changed in version 3.3:** Previous versions compared the raw memory disregarding the item format and the logical array structure.

<a id="memoryviewtobytes"></a>

### `memoryview.tobytes(order='C')`

Return the data in the buffer as a bytestring. This is equivalent to calling the bytes constructor on the memoryview.

```python
m = memoryview(b"abc")
m.tobytes()
b'abc'
```

<a id="memoryviewhex"></a>

### `memoryview.hex(sep, bytes_per_sep=1)`

Return a string object containing two hexadecimal digits for each byte in the buffer.

```python
m = memoryview(b"abc")
m.hex()
'616263'
```

> **Added in version 3.5.**

> **Changed in version 3.8:** Similar to bytes.hex(), memoryview.hex() now supports optional sep and bytes_per_sep parameters to insert separators between bytes in the hex output.

<a id="memoryviewtolist"></a>

### `memoryview.tolist()`

Return the data in the buffer as a list of elements.

<a id="memoryviewtoreadonly"></a>

### `memoryview.toreadonly()`

Return a readonly version of the memoryview object. The original memoryview object is unchanged.

```python
m = memoryview(bytearray(b'abc'))
mm = m.toreadonly()
mm.tolist()
[97, 98, 99]
mm[0] = 42
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot modify read-only memory
m[0] = 43
mm.tolist()
[43, 98, 99]
```

> **Added in version 3.8.**

<a id="memoryviewrelease"></a>

### `memoryview.release()`

Release the underlying buffer exposed by the memoryview object. Many objects take special actions when a view is held on them (for example, a bytearray would temporarily forbid resizing); therefore, calling release() is handy to remove these restrictions (and free any dangling resources) as soon as possible.

After this method has been called, any further operation on the view raises a ValueError (except release() itself which can be called multiple times):

```python
m = memoryview(b'abc')
m.release()
m[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: operation forbidden on released memoryview object
```

The context management protocol can be used for a similar effect, using the with statement:

with memoryview(b'abc') as m:

m[0]

```python
97
m[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: operation forbidden on released memoryview object
```

> **Added in version 3.2.**

<a id="memoryviewcast"></a>

### `memoryview.cast(format, shape, /)`

Cast a memoryview to a new format or shape. shape defaults to [byte_length//new_itemsize], which means that the result view will be one-dimensional. The return value is a new memoryview, but the buffer itself is not copied. Supported casts are 1D -> C-contiguous and C-contiguous -> 1D.

The destination format is restricted to a single element native format in struct syntax. One of the formats must be a byte format (‘B’, ‘b’ or ‘c’). The byte length of the result must be the same as the original length. Note that all byte lengths may depend on the operating system.

Cast 1D/long to 1D/unsigned bytes:

```python
import array
a = array.array('l', [1,2,3])
x = memoryview(a)
x.format
'l'
x.itemsize
8
```

<a id="memoryviewcount"></a>

### `memoryview.count(value, /)`

Count the number of occurrences of value.

> **Added in version 3.14.**

<a id="memoryviewindex"></a>

### `memoryview.index(value, start=0, stop=sys.maxsize, /)`

Return the index of the first occurrence of value (at or after index start and before index stop).

Raises a ValueError if value cannot be found.

> **Added in version 3.14.**

### Read-only attributes

#### `memoryview.obj`

The underlying object of the memoryview:

```python
b  = bytearray(b'xyz')
m = memoryview(b)
m.obj is b
True
```

> **Added in version 3.3.**

#### `memoryview.nbytes`

```python
nbytes == product(shape) * itemsize == len(m.tobytes()). This is the amount of space in bytes that the array would use in a contiguous representation. It is not necessarily equal to len(m):
import array
a = array.array('i', [1,2,3,4,5])
m = memoryview(a)
len(m)
5
m.nbytes
20
y = m[::2]
len(y)
3
y.nbytes
12
len(y.tobytes())
12
```

Multi-dimensional arrays:

```python
import struct
buf = struct.pack("d"*12, *[1.5*x for x in range(12)])
x = memoryview(buf)
y = x.cast('d', shape=[3,4])
y.tolist()
[[0.0, 1.5, 3.0, 4.5], [6.0, 7.5, 9.0, 10.5], [12.0, 13.5, 15.0, 16.5]]
len(y)
3
y.nbytes
96
```

> **Added in version 3.3.**

#### `memoryview.readonly`

A bool indicating whether the memory is read only.

#### `memoryview.format`

A string containing the format (in struct module style) for each element in the view. A memoryview can be created from exporters with arbitrary format strings, but some methods (e.g. tolist()) are restricted to native single element formats.

> **Changed in version 3.3:** format 'B' is now handled according to the struct module syntax. This means that memoryview(b'abc')[0] == b'abc'[0] == 97.

#### `memoryview.itemsize`

The size in bytes of each element of the memoryview:

```python
import array, struct
m = memoryview(array.array('H', [32000, 32001, 32002]))
m.itemsize
2
m[0]
32000
struct.calcsize('H') == m.itemsize
True
```

#### `memoryview.ndim`

An integer indicating how many dimensions of a multi-dimensional array the memory represents.

#### `memoryview.shape`

A tuple of integers the length of ndim giving the shape of the memory as an N-dimensional array.

> **Changed in version 3.3:** An empty tuple instead of None when ndim = 0.

#### `memoryview.strides`

A tuple of integers the length of ndim giving the size in bytes to access each element for each dimension of the array.

> **Changed in version 3.3:** An empty tuple instead of None when ndim = 0.

#### `memoryview.suboffsets`

Used internally for PIL-style arrays. The value is informational only.

#### `memoryview.c_contiguous`

A bool indicating whether the memory is C-contiguous.

> **Added in version 3.3.**

#### `memoryview.f_contiguous`

A bool indicating whether the memory is Fortran contiguous.

> **Added in version 3.3.**

#### `memoryview.contiguous`

A bool indicating whether the memory is contiguous.

> **Added in version 3.3.**

**See also:** [Thread safety for memoryview objects](https://docs.python.org/3/library/stdtypes.html#thread-safety-for-memoryview-objects) in the free-threaded build.

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Text Sequence Type — str](../text-sequence-type-str/index.md) | `str.encode()` / `bytes.decode()` and text processing paired with binary data. |
| [Common Sequence Operations](../sequence-types-list-tuple-range/common-sequence-operations/index.md) | Indexing, slicing, and `in` shared by bytes-like types, lists, and tuples. |
