# [Text Sequence Type — str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)

Textual data in Python is represented by **`str`** objects—**strings**. A string is an **immutable sequence of Unicode code points**: you can index and slice it like other sequences, but you cannot change a character in place. Full specification and edge cases remain on [docs.python.org](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str); this page explains how strings fit into everyday programming and how each major API behaves.

---

## Role of `str` in Python programs

Strings are the default type for **human-readable text**, **identifiers**, **paths**, **URLs**, **JSON text**, and most data read from or written to files and networks after decoding. Because there is **no separate character type**, a single “character” is simply a string of length 1—for example `s[0]` and `s[0:1]` are equal for non-empty `s`.

Immutability means every “change” builds a **new** string. For many small concatenations, `str.join()` on a list of fragments (or `io.StringIO`) is more efficient than repeated `+`.

Strings implement all [**common sequence operations**](../sequence-types-list-tuple-range/common-sequence-operations/index.md) (indexing, slicing, membership, concatenation, repetition, length). They do **not** support mutable-sequence assignment (`s[i] = x`).

---

## String literals

Literal syntax is defined in [String and Bytes literals](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals). In practice you will use:

| Form | Example | When to use it |
|------|---------|----------------|
| Single-quoted | `'allows embedded "double" quotes'` | Default short text |
| Double-quoted | `"allows embedded 'single' quotes"` | Same as single; pick quotes that avoid escaping |
| Triple-quoted | `'''line1\nline2'''`, `"""doc"""` | Multiline strings; **all** indentation on those lines is kept |
| Adjacent literals | `"spam " "eggs"` → `"spam eggs"` | Implicit concatenation when only whitespace separates literals in one expression |
| Raw `r"..."` | `r'\n'` is backslash + `n`, not newline | Regex, Windows paths, literal backslashes |
| `u"..."` (3.3+) | No effect on meaning | Legacy Python 2 marker only; cannot combine with `r` |

```python
assert "spam " "eggs" == "spam eggs"
assert len('🐍') == 1
assert 'abc'[0] == 'abc'[0:1] == 'a'
```

> **Changed in version 3.3:** The `u` prefix is permitted again for compatibility; it does not alter string semantics.

---

## Constructing strings with `str()`

The built-in **`str`** constructor is overloaded. Behavior depends on whether you pass **`encoding`** or **`errors`**.

### Informal string (`str(object)`)

With no encoding arguments, `str(object)` calls `type(object).__str__(object)`—the **informal**, user-facing form. For an existing `str`, that is the string itself. Without `__str__`, Python falls back to `repr(object)`.

```python
assert str(42) == '42'
assert str('hi') == 'hi'
assert str(b'Zoot!') == "b'Zoot!'"
```

### Decoding bytes (`str(bytes, encoding, errors='strict')`)

When **`encoding`** or **`errors`** is supplied, `object` must be **bytes-like**. `str(b, enc, err)` is equivalent to `b.decode(enc, err)`. See [Binary Sequence Types — bytes, bytearray, memoryview](../binary-sequence-types-bytes-bytearray-memoryview/index.md).

```python
raw = 'Python'.encode('utf-8')
assert str(raw, 'utf-8') == 'Python'
assert str() == ''
```

---

## String methods — overview

Strings add many methods beyond shared sequence operators. They also support **f-strings**, **`str.format()`**, and legacy **`%` printf-style** formatting.

The [**Text Processing Services**](https://docs.python.org/3/library/text.html) library (`re`, `json`, `pathlib`, etc.) builds on these primitives.

## String methods (reference)

| Method | Category | Typical use |
|--------|----------|-------------|
| [`str.find()`](#strfind) | Search, test, and count | find where substrings occur, test boundaries, or count matches |
| [`str.rfind()`](#strrfind) | Search, test, and count | find where substrings occur, test boundaries, or count matches |
| [`str.index()`](#strindex) | Search, test, and count | find where substrings occur, test boundaries, or count matches |
| [`str.rindex()`](#strrindex) | Search, test, and count | find where substrings occur, test boundaries, or count matches |
| [`str.count()`](#strcount) | Search, test, and count | find where substrings occur, test boundaries, or count matches |
| [`str.startswith()`](#strstartswith) | Search, test, and count | find where substrings occur, test boundaries, or count matches |
| [`str.endswith()`](#strendswith) | Search, test, and count | find where substrings occur, test boundaries, or count matches |
| [`str.split()`](#strsplit) | Split, join, and partition | break text apart or concatenate iterables of strings |
| [`str.rsplit()`](#strrsplit) | Split, join, and partition | break text apart or concatenate iterables of strings |
| [`str.splitlines()`](#strsplitlines) | Split, join, and partition | break text apart or concatenate iterables of strings |
| [`str.partition()`](#strpartition) | Split, join, and partition | break text apart or concatenate iterables of strings |
| [`str.rpartition()`](#strrpartition) | Split, join, and partition | break text apart or concatenate iterables of strings |
| [`str.join()`](#strjoin) | Split, join, and partition | break text apart or concatenate iterables of strings |
| [`str.strip()`](#strstrip) | Strip, prefix, and suffix | trim edges or remove/add fixed affixes |
| [`str.lstrip()`](#strlstrip) | Strip, prefix, and suffix | trim edges or remove/add fixed affixes |
| [`str.rstrip()`](#strrstrip) | Strip, prefix, and suffix | trim edges or remove/add fixed affixes |
| [`str.removeprefix()`](#strremoveprefix) | Strip, prefix, and suffix | trim edges or remove/add fixed affixes |
| [`str.removesuffix()`](#strremovesuffix) | Strip, prefix, and suffix | trim edges or remove/add fixed affixes |
| [`str.capitalize()`](#strcapitalize) | Case and title | change letter case for display or comparisons |
| [`str.casefold()`](#strcasefold) | Case and title | change letter case for display or comparisons |
| [`str.lower()`](#strlower) | Case and title | change letter case for display or comparisons |
| [`str.upper()`](#strupper) | Case and title | change letter case for display or comparisons |
| [`str.swapcase()`](#strswapcase) | Case and title | change letter case for display or comparisons |
| [`str.title()`](#strtitle) | Case and title | change letter case for display or comparisons |
| [`str.center()`](#strcenter) | Padding and alignment | pad or align text in a fixed-width field |
| [`str.ljust()`](#strljust) | Padding and alignment | pad or align text in a fixed-width field |
| [`str.rjust()`](#strrjust) | Padding and alignment | pad or align text in a fixed-width field |
| [`str.zfill()`](#strzfill) | Padding and alignment | pad or align text in a fixed-width field |
| [`str.expandtabs()`](#strexpandtabs) | Padding and alignment | pad or align text in a fixed-width field |
| [`str.replace()`](#strreplace) | Transform and encode | replace content, map characters, or encode to bytes |
| [`str.translate()`](#strtranslate) | Transform and encode | replace content, map characters, or encode to bytes |
| [`str.encode()`](#strencode) | Transform and encode | replace content, map characters, or encode to bytes |
| [`str.format()`](#strformat) | Formatting helpers | build strings from templates or mappings |
| [`str.format_map()`](#strformat_map) | Formatting helpers | build strings from templates or mappings |
| [`str.isalnum()`](#strisalnum) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isalpha()`](#strisalpha) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isascii()`](#strisascii) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isdecimal()`](#strisdecimal) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isdigit()`](#strisdigit) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isidentifier()`](#strisidentifier) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.islower()`](#strislower) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isnumeric()`](#strisnumeric) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isprintable()`](#strisprintable) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isspace()`](#strisspace) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.istitle()`](#stristitle) | Classification (`is*` methods) | test Unicode categories and identifier rules |
| [`str.isupper()`](#strisupper) | Classification (`is*` methods) | test Unicode categories and identifier rules |

---

### Search, test, and count

Methods in this group find where substrings occur, test boundaries, or count matches. Each returns a **new** string (or list/bool) unless noted; the original `str` is unchanged.

<a id="strfind"></a>

### `str.find(sub[, start[, end]])`

Return the lowest index in the string where substring sub is found within the slice s[start:end]. Optional arguments start and end are interpreted as in slice notation. Return -1 if sub is not found. For example:

```python
'spam, spam, spam'.find('sp')
0
'spam, spam, spam'.find('sp', 5)
6
```

**See also:** rfind() and index().

!!! note
    The find() method should be used only if you need to know the position of sub. To check if sub is a substring or not, use the in operator:

```python
'Py' in 'Python'
True
```

<a id="strrfind"></a>

### `str.rfind(sub[, start[, end]])`

Return the highest index in the string where substring sub is found, such that sub is contained within s[start:end]. Optional arguments start and end are interpreted as in slice notation. Return -1 on failure. For example:

```python
'spam, spam, spam'.rfind('sp')
12
'spam, spam, spam'.rfind('sp', 0, 10)
6
```

**See also:** find() and rindex().

<a id="strindex"></a>

### `str.index(sub[, start[, end]])`

Like find(), but raise ValueError when the substring is not found. For example:

```python
'spam, spam, spam'.index('spam')
0
'spam, spam, spam'.index('eggs')
Traceback (most recent call last):
  File "<python-input-0>", line 1, in <module>
    'spam, spam, spam'.index('eggs')
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
ValueError: substring not found
```

**See also:** rindex().

<a id="strrindex"></a>

### `str.rindex(sub[, start[, end]])`

Like rfind() but raises ValueError when the substring sub is not found. For example:

```python
'spam, spam, spam'.rindex('spam')
12
'spam, spam, spam'.rindex('eggs')
Traceback (most recent call last):
  File "<stdin-0>", line 1, in <module>
    'spam, spam, spam'.rindex('eggs')
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
ValueError: substring not found
```

**See also:** index() and find().

<a id="strcount"></a>

### `str.count(sub[, start[, end]])`

Return the number of non-overlapping occurrences of substring sub in the range [start, end]. Optional arguments start and end are interpreted as in slice notation.

If sub is empty, returns the number of empty strings between characters which is the length of the string plus one. For example:

```python
'spam, spam, spam'.count('spam')
3
'spam, spam, spam'.count('spam', 5)
2
'spam, spam, spam'.count('spam', 5, 10)
1
'spam, spam, spam'.count('eggs')
0
'spam, spam, spam'.count('')
17
```

<a id="strstartswith"></a>

### `str.startswith(prefix[, start[, end]])`

Return True if string starts with the prefix, otherwise return False. prefix can also be a tuple of prefixes to look for. With optional start, test string beginning at that position. With optional end, stop comparing string at that position.

For example:

```python
'Python'.startswith('Py')
True
'a tuple of prefixes'.startswith(('at', 'a'))
True
'Python is amazing'.startswith('is', 7)
True
```

**See also:** endswith() and removeprefix().

<a id="strendswith"></a>

### `str.endswith(suffix[, start[, end]])`

Return True if the string ends with the specified suffix, otherwise return False. suffix can also be a tuple of suffixes to look for. With optional start, test beginning at that position. With optional end, stop comparing at that position. Using start and end is equivalent to str[start:end].endswith(suffix). For example:

```python
'Python'.endswith('on')
True
'a tuple of suffixes'.endswith(('at', 'in'))
False
'a tuple of suffixes'.endswith(('at', 'es'))
True
'Python is amazing'.endswith('is', 0, 9)
True
```

**See also:** startswith() and removesuffix().

---

### Split, join, and partition

Methods in this group break text apart or concatenate iterables of strings. Each returns a **new** string (or list/bool) unless noted; the original `str` is unchanged.

<a id="strsplit"></a>

### `str.split(sep=None, maxsplit=-1)`

Return a list of the words in the string, using sep as the delimiter string. If maxsplit is given, at most maxsplit splits are done (thus, the list will have at most maxsplit+1 elements). If maxsplit is not specified or -1, then there is no limit on the number of splits (all possible splits are made).

If sep is given, consecutive delimiters are not grouped together and are deemed to delimit empty strings (for example, '1,,2'.split(',') returns ['1', '', '2']). The sep argument may consist of multiple characters as a single delimiter (to split with multiple delimiters, use re.split()). Splitting an empty string with a specified separator returns [''].

For example:

```python
'1,2,3'.split(',')
['1', '2', '3']
'1,2,3'.split(',', maxsplit=1)
['1', '2,3']
'1,2,,3,'.split(',')
['1', '2', '', '3', '']
'1<>2<>3<4'.split('<>')
['1', '2', '3<4']
```

If sep is not specified or is None, a different splitting algorithm is applied: runs of consecutive whitespace are regarded as a single separator, and the result will contain no empty strings at the start or end if the string has leading or trailing whitespace. Consequently, splitting an empty string or a string consisting of just whitespace with a None separator returns [].

For example:

```python
'1 2 3'.split()
['1', '2', '3']
'1 2 3'.split(maxsplit=1)
['1', '2 3']
'   1   2   3   '.split()
['1', '2', '3']
```

If sep is not specified or is None and maxsplit is 0, only leading runs of consecutive whitespace are considered.

For example:

```python
"".split(None, 0)
[]
"   ".split(None, 0)
[]
"   foo   ".split(maxsplit=0)
['foo   ']
```

**See also:** join().

<a id="strrsplit"></a>

### `str.rsplit(sep=None, maxsplit=-1)`

Return a list of the words in the string, using sep as the delimiter string. If maxsplit is given, at most maxsplit splits are done, the rightmost ones. If sep is not specified or None, any whitespace string is a separator. Except for splitting from the right, rsplit() behaves like split() which is described in detail below.

<a id="strsplitlines"></a>

Line boundaries recognized by `splitlines()` (superset of universal newlines):


| Escape / code | Description |
|---------------|-------------|
| `\n` | Line Feed |
| `\r` | Carriage Return |
| `\r\n` | Carriage Return + Line Feed |
| `\v`, `\x0b` | Line Tabulation |
| `\f`, `\x0c` | Form Feed |
| `\x1c` | File Separator |
| `\x1d` | Group Separator |
| `\x1e` | Record Separator |
| `\x85` | Next Line (C1) |
| `\u2028` | Line Separator |
| `\u2029` | Paragraph Separator |

> **Changed in version 3.2:** `\v` and `\f` are recognized as line boundaries.

### `str.splitlines(keepends=False)`

Return a list of the lines in the string, breaking at line boundaries. Line breaks are not included in the resulting list unless keepends is given and true.

This method splits on the following line boundaries. In particular, the boundaries are a superset of universal newlines.

Representation

Description

\n

Line Feed

\r

Carriage Return

\r\n

Carriage Return + Line Feed

\v or \x0b

Line Tabulation

\f or \x0c

Form Feed

\x1c

```python
File Separator
\x1d
```

Group Separator

\x1e

Record Separator

\x85

Next Line (C1 Control Code)

\u2028

Line Separator

\u2029

Paragraph Separator

> **Changed in version 3.2:** \v and \f added to list of line boundaries.

For example:

```python
'ab c\n\nde fg\rkl\r\n'.splitlines()
['ab c', '', 'de fg', 'kl']
'ab c\n\nde fg\rkl\r\n'.splitlines(keepends=True)
['ab c\n', '\n', 'de fg\r', 'kl\r\n']
```

Unlike split() when a delimiter string sep is given, this method returns an empty list for the empty string, and a terminal line break does not result in an extra line:

```python
"".splitlines()
[]
"One line\n".splitlines()
['One line']
```

For comparison, split('\n') gives:

```python
''.split('\n')
['']
'Two lines\n'.split('\n')
['Two lines', '']
```

<a id="strpartition"></a>

### `str.partition(sep, /)`

Split the string at the first occurrence of sep, and return a 3-tuple containing the part before the separator, the separator itself, and the part after the separator. If the separator is not found, return a 3-tuple containing the string itself, followed by two empty strings.

For example:

```python
'Monty Python'.partition(' ')
('Monty', ' ', 'Python')
"Monty Python's Flying Circus".partition(' ')
('Monty', ' ', "Python's Flying Circus")
'Monty Python'.partition('-')
('Monty Python', '', '')
```

**See also:** rpartition().

<a id="strrpartition"></a>

### `str.rpartition(sep, /)`

Split the string at the last occurrence of sep, and return a 3-tuple containing the part before the separator, the separator itself, and the part after the separator. If the separator is not found, return a 3-tuple containing two empty strings, followed by the string itself.

For example:

```python
'Monty Python'.rpartition(' ')
('Monty', ' ', 'Python')
"Monty Python's Flying Circus".rpartition(' ')
("Monty Python's Flying", ' ', 'Circus')
'Monty Python'.rpartition('-')
('', '', 'Monty Python')
```

**See also:** partition().

<a id="strjoin"></a>

### `str.join(iterable, /)`

Return a string which is the concatenation of the strings in iterable. A TypeError will be raised if there are any non-string values in iterable, including bytes objects. The separator between elements is the string providing this method. For example:

```python
', '.join(['spam', 'spam', 'spam'])
'spam, spam, spam'
'-'.join('Python')
'P-y-t-h-o-n'
```

**See also:** split().

---

### Strip, prefix, and suffix

Methods in this group trim edges or remove/add fixed affixes. Each returns a **new** string (or list/bool) unless noted; the original `str` is unchanged.

<a id="strstrip"></a>

### `str.strip(chars=None, /)`

Return a copy of the string with the leading and trailing characters removed. The chars argument is a string specifying the set of characters to be removed. If omitted or None, the chars argument defaults to removing whitespace. The chars argument is not a prefix or suffix; rather, all combinations of its values are stripped.

Whitespace characters are defined by str.isspace().

For example:

```python
'   spacious   '.strip()
'spacious'
'www.example.com'.strip('cmowz.')
'example'
```

The outermost leading and trailing chars argument values are stripped from the string. Characters are removed from the leading end until reaching a string character that is not contained in the set of characters in chars. A similar action takes place on the trailing end.

For example:

comment_string = '#....... Section 3.2.1 Issue #32 .......'

```python
comment_string.strip('.#! ')
'Section 3.2.1 Issue #32'
```

**See also:** rstrip().

<a id="strlstrip"></a>

### `str.lstrip(chars=None, /)`

Return a copy of the string with leading characters removed. The chars argument is a string specifying the set of characters to be removed. If omitted or None, the chars argument defaults to removing whitespace. The chars argument is not a prefix; rather, all combinations of its values are stripped:

```python
'   spacious   '.lstrip()
'spacious   '
'www.example.com'.lstrip('cmowz.')
'example.com'
```

See str.removeprefix() for a method that will remove a single prefix string rather than all of a set of characters. For example:

```python
'Arthur: three!'.lstrip('Arthur: ')
'ee!'
'Arthur: three!'.removeprefix('Arthur: ')
'three!'
static str.maketrans(dict, /)
static str.maketrans(from, to, remove='', /)
This static method returns a translation table usable for str.translate().
```

If there is only one argument, it must be a dictionary mapping Unicode ordinals (integers) or characters (strings of length 1) to Unicode ordinals, strings (of arbitrary lengths) or None. Character keys will then be converted to ordinals.

If there are two arguments, they must be strings of equal length, and in the resulting dictionary, each character in from will be mapped to the character at the same position in to. If there is a third argument, it must be a string, whose characters will be mapped to None in the result.

<a id="strrstrip"></a>

### `str.rstrip(chars=None, /)`

Return a copy of the string with trailing characters removed. The chars argument is a string specifying the set of characters to be removed. If omitted or None, the chars argument defaults to removing whitespace. The chars argument is not a suffix; rather, all combinations of its values are stripped. For example:

```python
'   spacious   '.rstrip()
'   spacious'
'mississippi'.rstrip('ipz')
'mississ'
```

See removesuffix() for a method that will remove a single suffix string rather than all of a set of characters. For example:

```python
'Monty Python'.rstrip(' Python')
'M'
'Monty Python'.removesuffix(' Python')
'Monty'
```

**See also:** strip().

<a id="strremoveprefix"></a>

### `str.removeprefix(prefix, /)`

If the string starts with the prefix string, return string[len(prefix):]. Otherwise, return a copy of the original string:

```python
'TestHook'.removeprefix('Test')
'Hook'
'BaseTestCase'.removeprefix('Test')
'BaseTestCase'
```

Added in version 3.9.

**See also:** removesuffix() and startswith().

<a id="strremovesuffix"></a>

### `str.removesuffix(suffix, /)`

If the string ends with the suffix string and that suffix is not empty, return string[:-len(suffix)]. Otherwise, return a copy of the original string:

```python
'MiscTests'.removesuffix('Tests')
'Misc'
'TmpDirMixin'.removesuffix('Tests')
'TmpDirMixin'
```

Added in version 3.9.

**See also:** removeprefix() and endswith().

---

### Case and title

Methods in this group change letter case for display or comparisons. Each returns a **new** string (or list/bool) unless noted; the original `str` is unchanged.

<a id="strcapitalize"></a>

### `str.capitalize()`

Return a copy of the string with its first character capitalized and the rest lowercased.

> **Changed in version 3.8:** The first character is now put into titlecase rather than uppercase. This means that characters like digraphs will only have their first letter capitalized, instead of the full character.

<a id="strcasefold"></a>

### `str.casefold()`

Return a casefolded copy of the string. Casefolded strings may be used for caseless matching.

Casefolding is similar to lowercasing but more aggressive because it is intended to remove all case distinctions in a string. For example, the German lowercase letter 'ß' is equivalent to "ss". Since it is already lowercase, lower() would do nothing to 'ß'; casefold() converts it to "ss". For example:

```python
'straße'.lower()
'straße'
'straße'.casefold()
'strasse'
```

The casefolding algorithm is described in section 3.13 ‘Default Case Folding’ of the Unicode Standard.

Added in version 3.3.

<a id="strlower"></a>

### `str.lower()`

Return a copy of the string with all the cased characters [4] converted to lowercase. For example:

```python
'Lower Method Example'.lower()
'lower method example'
```

The lowercasing algorithm used is described in section 3.13 ‘Default Case Folding’ of the Unicode Standard.

<a id="strupper"></a>

### `str.upper()`

Return a copy of the string with all the cased characters [4] converted to uppercase. Note that s.upper().isupper() might be False if s contains uncased characters or if the Unicode category of the resulting character(s) is not “Lu” (Letter, uppercase), but e.g. “Lt” (Letter, titlecase).

The uppercasing algorithm used is described in section 3.13 ‘Default Case Folding’ of the Unicode Standard.

<a id="strswapcase"></a>

### `str.swapcase()`

Return a copy of the string with uppercase characters converted to lowercase and vice versa. For example:

```python
'Hello World'.swapcase()
'hELLO wORLD'
```

!!! note
    that it is not necessarily true that s.swapcase().swapcase() == s. For example:

```python
'straße'.swapcase().swapcase()
'strasse'
```

**See also:** str.lower() and str.upper().

<a id="strtitle"></a>

### `str.title()`

Return a titlecased version of the string where words start with an uppercase character and the remaining characters are lowercase.

For example:

```python
'Hello world'.title()
'Hello World'
```

The algorithm uses a simple language-independent definition of a word as groups of consecutive letters. The definition works in many contexts but it means that apostrophes in contractions and possessives form word boundaries, which may not be the desired result:

```python
"they're bill's friends from the UK".title()
"They'Re Bill'S Friends From The Uk"
```

The string.capwords() function does not have this problem, as it splits words on spaces only.

Alternatively, a workaround for apostrophes can be constructed using regular expressions:

import re

def titlecase(s):

return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",

lambda mo: mo.group(0).capitalize(),

s)

```python
titlecase("they're bill's friends.")
"They're Bill's Friends."
```

**See also:** istitle().

---

### Padding and alignment

Methods in this group pad or align text in a fixed-width field. Each returns a **new** string (or list/bool) unless noted; the original `str` is unchanged.

<a id="strcenter"></a>

### `str.center(width, fillchar=' ', /)`

Return centered in a string of length width. Padding is done using the specified fillchar (default is an ASCII space). The original string is returned if width is less than or equal to len(s). For example:

```python
'Python'.center(10)
'  Python  '
'Python'.center(10, '-')
'--Python--'
'Python'.center(4)
'Python'
```

<a id="strljust"></a>

### `str.ljust(width, fillchar=' ', /)`

Return the string left justified in a string of length width. Padding is done using the specified fillchar (default is an ASCII space). The original string is returned if width is less than or equal to len(s).

For example:

```python
'Python'.ljust(10)
'Python    '
'Python'.ljust(10, '.')
'Python....'
'Monty Python'.ljust(10, '.')
'Monty Python'
```

**See also:** rjust().

<a id="strrjust"></a>

### `str.rjust(width, fillchar=' ', /)`

Return the string right justified in a string of length width. Padding is done using the specified fillchar (default is an ASCII space). The original string is returned if width is less than or equal to len(s).

For example:

```python
'Python'.rjust(10)
'    Python'
'Python'.rjust(10, '.')
'....Python'
'Monty Python'.rjust(10, '.')
'Monty Python'
```

**See also:** ljust() and zfill().

<a id="strzfill"></a>

### `str.zfill(width, /)`

Return a copy of the string left filled with ASCII '0' digits to make a string of length width. A leading sign prefix ('+'/'-') is handled by inserting the padding after the sign character rather than before. The original string is returned if width is less than or equal to len(s).

For example:

```python
"42".zfill(5)
'00042'
"-42".zfill(5)
'-0042'
```

**See also:** rjust().

<a id="strexpandtabs"></a>

### `str.expandtabs(tabsize=8)`

Return a copy of the string where all tab characters are replaced by one or more spaces, depending on the current column and the given tab size. Tab positions occur every tabsize characters (default is 8, giving tab positions at columns 0, 8, 16 and so on). To expand the string, the current column is set to zero and the string is examined character by character. If the character is a tab (\t), one or more space characters are inserted in the result until the current column is equal to the next tab position. (The tab character itself is not copied.) If the character is a newline (\n) or return (\r), it is copied and the current column is reset to zero. Any other character is copied unchanged and the current column is incremented by one regardless of how the character is represented when printed. For example:

```python
'01\t012\t0123\t01234'.expandtabs()
'01      012     0123    01234'
'01\t012\t0123\t01234'.expandtabs(4)
'01  012 0123    01234'
print('01\t012\n0123\t01234'.expandtabs(4))
01  012
0123    01234
```

---

### Transform and encode

Methods in this group replace content, map characters, or encode to bytes. Each returns a **new** string (or list/bool) unless noted; the original `str` is unchanged.

<a id="strreplace"></a>

### `str.replace(old, new, /, count=-1)`

Return a copy of the string with all occurrences of substring old replaced by new. If count is given, only the first count occurrences are replaced. If count is not specified or -1, then all occurrences are replaced. For example:

```python
'spam, spam, spam'.replace('spam', 'eggs')
'eggs, eggs, eggs'
'spam, spam, spam'.replace('spam', 'eggs', 1)
'eggs, spam, spam'
```

> **Changed in version 3.13:** count is now supported as a keyword argument.

<a id="strtranslate"></a>

### `str.translate(table, /)`

Return a copy of the string in which each character has been mapped through the given translation table. The table must be an object that implements indexing via __getitem__(), typically a mapping or sequence. When indexed by a Unicode ordinal (an integer), the table object can do any of the following: return a Unicode ordinal or a string, to map the character to one or more other characters; return None, to delete the character from the return string; or raise a LookupError exception, to map the character to itself.

You can use str.maketrans() to create a translation map from character-to-character mappings in different formats.

**See also:** the codecs module for a more flexible approach to custom character mappings.

<a id="strencode"></a>

### `str.encode(encoding='utf-8', errors='strict')`

Return the string encoded to bytes.

encoding defaults to 'utf-8'; see Standard Encodings for possible values.

errors controls how encoding errors are handled. If 'strict' (the default), a UnicodeError exception is raised. Other possible values are 'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace' and any other name registered via codecs.register_error(). See Error Handlers for details.

For performance reasons, the value of errors is not checked for validity unless an encoding error actually occurs, Python Development Mode is enabled or a debug build is used. For example:

encoded_str_to_bytes = 'Python'.encode()

```python
type(encoded_str_to_bytes)
<class 'bytes'>
encoded_str_to_bytes
b'Python'
```

> **Changed in version 3.1:** Added support for keyword arguments.

> **Changed in version 3.9:** The value of the errors argument is now checked in Python Development Mode and in debug mode.

---

### Formatting helpers

Methods in this group build strings from templates or mappings. Each returns a **new** string (or list/bool) unless noted; the original `str` is unchanged.

<a id="strformat"></a>

### `str.format(*args, **kwargs)`

Perform a string formatting operation. The string on which this method is called can contain literal text or replacement fields delimited by braces {}. Each replacement field contains either the numeric index of a positional argument, or the name of a keyword argument. Returns a copy of the string where each replacement field is replaced with the string value of the corresponding argument. For example:

```python
"The sum of 1 + 2 is {0}".format(1+2)
'The sum of 1 + 2 is 3'
"The sum of {a} + {b} is {answer}".format(answer=1+2, a=1, b=2)
'The sum of 1 + 2 is 3'
"{1} expects the {0} Inquisition!".format("Spanish", "Nobody")
'Nobody expects the Spanish Inquisition!'
```

See Format string syntax for a description of the various formatting options that can be specified in format strings.

!!! note
    When formatting a number (int, float, complex, decimal.Decimal and subclasses) with the n type (ex: '{:n}'.format(1234)), the function temporarily sets the LC_CTYPE locale to the LC_NUMERIC locale to decode decimal_point and thousands_sep fields of localeconv() if they are non-ASCII or longer than 1 byte, and the LC_NUMERIC locale is different than the LC_CTYPE locale. This temporary change affects other threads.

> **Changed in version 3.7:** When formatting a number with the n type, the function sets temporarily the LC_CTYPE locale to the LC_NUMERIC locale in some cases.

<a id="strformat_map"></a>

### `str.format_map(mapping, /)`

Similar to str.format(**mapping), except that mapping is used directly and not copied to a dict. This is useful if for example mapping is a dict subclass:

class Default(dict):

def __missing__(self, key):

return key

```python
'{name} was born in {country}'.format_map(Default(name='Guido'))
'Guido was born in country'
```

Added in version 3.2.

---

### Classification (`is*` methods)

Methods in this group test Unicode categories and identifier rules. Each returns a **new** string (or list/bool) unless noted; the original `str` is unchanged.

<a id="strisalnum"></a>

### `str.isalnum()`

Return True if all characters in the string are alphanumeric and there is at least one character, False otherwise. A character c is alphanumeric if one of the following returns True: c.isalpha(), c.isdecimal(), c.isdigit(), or c.isnumeric(). For example:

```python
'abc123'.isalnum()
True
'abc123!@#'.isalnum()
False
''.isalnum()
False
' '.isalnum()
False
```

<a id="strisalpha"></a>

### `str.isalpha()`

Return True if all characters in the string are alphabetic and there is at least one character, False otherwise. Alphabetic characters are those characters defined in the Unicode character database as “Letter”, i.e., those with general category property being one of “Lm”, “Lt”, “Lu”, “Ll”, or “Lo”. Note that this is different from the Alphabetic property defined in the section 4.10 ‘Letters, Alphabetic, and Ideographic’ of the Unicode Standard. For example:

```python
'Letters and spaces'.isalpha()
False
'LettersOnly'.isalpha()
True
'µ'.isalpha()  # non-ASCII characters can be considered alphabetical too
True
```

See Unicode Properties.

<a id="strisascii"></a>

### `str.isascii()`

Return True if the string is empty or all characters in the string are ASCII, False otherwise. ASCII characters have code points in the range U+0000-U+007F. For example:

```python
'ASCII characters'.isascii()
True
'µ'.isascii()
False
```

Added in version 3.7.

<a id="strisdecimal"></a>

### `str.isdecimal()`

Return True if all characters in the string are decimal characters and there is at least one character, False otherwise. Decimal characters are those that can be used to form numbers in base 10, such as U+0660, ARABIC-INDIC DIGIT ZERO. Formally a decimal character is a character in the Unicode General Category “Nd”. For example:

```python
'0123456789'.isdecimal()
True
'٠١٢٣٤٥٦٧٨٩'.isdecimal()  # Arabic-Indic digits zero to nine
True
'alphabetic'.isdecimal()
False
```

<a id="strisdigit"></a>

### `str.isdigit()`

Return True if all characters in the string are digits and there is at least one character, False otherwise. Digits include decimal characters and digits that need special handling, such as the compatibility superscript digits. This covers digits which cannot be used to form numbers in base 10, like the Kharosthi numbers. Formally, a digit is a character that has the property value Numeric_Type=Digit or Numeric_Type=Decimal.

<a id="strisidentifier"></a>

### `str.isidentifier()`

Return True if the string is a valid identifier according to the language definition, section Names (identifiers and keywords).

keyword.iskeyword() can be used to test whether string s is a reserved identifier, such as def and class.

Example:

from keyword import iskeyword

```python
'hello'.isidentifier(), iskeyword('hello')
(True, False)
'def'.isidentifier(), iskeyword('def')
(True, True)
```

<a id="strislower"></a>

### `str.islower()`

Return True if all cased characters [4] in the string are lowercase and there is at least one cased character, False otherwise.

<a id="strisnumeric"></a>

### `str.isnumeric()`

Return True if all characters in the string are numeric characters, and there is at least one character, False otherwise. Numeric characters include digit characters, and all characters that have the Unicode numeric value property, e.g. U+2155, VULGAR FRACTION ONE FIFTH. Formally, numeric characters are those with the property value Numeric_Type=Digit, Numeric_Type=Decimal or Numeric_Type=Numeric. For example:

```python
'0123456789'.isnumeric()
True
'٠١٢٣٤٥٦٧٨٩'.isnumeric()  # Arabic-indic digit zero to nine
True
'⅕'.isnumeric()  # Vulgar fraction one fifth
True
'²'.isdecimal(), '²'.isdigit(),  '²'.isnumeric()
(False, True, True)
```

**See also:** isdecimal() and isdigit(). Numeric characters are a superset of decimal numbers.

<a id="strisprintable"></a>

### `str.isprintable()`

Return True if all characters in the string are printable, False if it contains at least one non-printable character.

Here “printable” means the character is suitable for repr() to use in its output; “non-printable” means that repr() on built-in types will hex-escape the character. It has no bearing on the handling of strings written to sys.stdout or sys.stderr.

The printable characters are those which in the Unicode character database (see unicodedata) have a general category in group Letter, Mark, Number, Punctuation, or Symbol (L, M, N, P, or S); plus the ASCII space 0x20. Nonprintable characters are those in group Separator or Other (Z or C), except the ASCII space.

For example:

```python
''.isprintable(), ' '.isprintable()
(True, True)
'\t'.isprintable(), '\n'.isprintable()
(False, False)
```

**See also:** isspace().

<a id="strisspace"></a>

### `str.isspace()`

Return True if there are only whitespace characters in the string and there is at least one character, False otherwise.

For example:

```python
''.isspace()
False
' '.isspace()
True
'\t\n'.isspace() # TAB and BREAK LINE
True
'\u3000'.isspace() # IDEOGRAPHIC SPACE
True
A character is whitespace if in the Unicode character database (see unicodedata), either its general category is Zs (“Separator, space”), or its bidirectional class is one of WS, B, or S.
```

**See also:** isprintable().

<a id="stristitle"></a>

### `str.istitle()`

Return True if the string is a titlecased string and there is at least one character, for example uppercase characters may only follow uncased characters and lowercase characters only cased ones. Return False otherwise.

For example:

```python
'Spam, Spam, Spam'.istitle()
True
'spam, spam, spam'.istitle()
False
'SPAM, SPAM, SPAM'.istitle()
False
```

**See also:** title().

<a id="strisupper"></a>

### `str.isupper()`

Return True if all cased characters [4] in the string are uppercase and there is at least one cased character, False otherwise.

```python
'BANANA'.isupper()
True
'banana'.isupper()
False
'baNana'.isupper()
False
' '.isupper()
False
```

---

## [Formatted String Literals (f-strings)](https://docs.python.org/3/library/stdtypes.html#formatted-string-literals-f-strings) {#formatted-string-literals-f-strings}


> **Added in version 3.6.**

> **Changed in version 3.7:** `await` and `async for` may appear in f-string expressions.

> **Changed in version 3.8:** Debug specifier `=` added.

> **Changed in version 3.12:** Many expression restrictions removed (nested strings, comments, backslashes allowed).

An **f-string** (formatted string literal) is prefixed with **`f`** or **`F`**. Curly braces `{…}` embed expressions evaluated at runtime. Each field may include, in order:

1. The **expression**
2. An optional **debug specifier** (`=`)
3. An optional **conversion** (`!s`, `!r`, `!a`)
4. An optional **format specifier** after `:`

See [f-strings in Lexical Analysis](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) for full syntax.

### Debug specifier (`=`)

> **Added in version 3.8.**

With `=`, the output includes the **expression source**, `=`, and the **value**—ideal for quick debugging:

```python
number = 14.3
assert f'{number=}' == 'number=14.3'
assert f'{ number  -  4  = }' == ' number  -  4  = 10.3'  # whitespace preserved
```

### Conversion specifiers (`!s`, `!r`, `!a`)

By default, values are converted with **`str()`**. With a debug specifier but **no** format specifier, **`repr()`** is used instead.

| Specifier | Calls | Typical use |
|-----------|-------|-------------|
| `!s` | `str()` | User-facing text |
| `!r` | `repr()` | Unambiguous, developer-oriented |
| `!a` | `ascii()` | ASCII-only escapes |

```python
from fractions import Fraction
one_third = Fraction(1, 3)
assert f'{one_third}' == '1/3'
assert f'{one_third = }' == 'one_third = Fraction(1, 3)'
assert f'{one_third!s} is {one_third!r}' == '1/3 is Fraction(1, 3)'
string = "¡kočka 😸!"
assert f'{string = !a}' == "string = '\xa1ko\u010dka \U0001f638!'"
```

### Format specifier (`:`)

After conversion, **`format()`** applies the part after `:`. Nested fields inside the format spec (e.g. `{amount:.{precision}f}`) are evaluated **eagerly**.

```python
from fractions import Fraction
one_third = Fraction(1, 3)
assert f'{one_third:.6f}' == '0.333333'
assert f'{one_third:_^+10}' == '___+1/3___'
assert f'{one_third!r:_^20}' == '___Fraction(1, 3)___'
assert f'{one_third = :~>10}~' == 'one_third = ~~~~~~~1/3~'
```

See [Format string syntax](https://docs.python.org/3/library/string.html#formatstrings) for the mini-language after `:`.
## [Template String Literals (t-strings)](https://docs.python.org/3/library/stdtypes.html#template-string-literals-t-strings) {#template-string-literals-t-strings}


A **t-string** (template string literal, **3.14+**) is prefixed with **`t`** or **`T`**. Syntax mirrors f-strings, but evaluation differs:

| Aspect | f-string | t-string |
|--------|----------|----------|
| Result type | `str` | `string.templatelib.Template` |
| Formatting | `format()` runs immediately | Specifiers become `Interpolation` objects for later processing |
| `=` debug | Uses `repr()` by default when no other conversion | Expression text appended to preceding literal; default conversion `r` unless overridden |

**Deferred formatting:** Code that consumes the `Template` decides how to interpret format specifiers and conversions—useful for safe templating where you must not evaluate arbitrary format logic at literal creation time.

**Nested format specs:** `{amount:.{precision}f}` evaluates `{precision}` first to build the format_spec (e.g. `'.2f'` when `precision` is `2`).

**Debug (`=`):** The expression text (including `=` and surrounding spaces) is appended to the literal portion; an `Interpolation` is still created, defaulting to repr conversion unless you supply an explicit conversion or format specifier.
## [printf-style String Formatting](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting) {#printf-style-string-formatting}


!!! note
    These operations have historical quirks (e.g. displaying tuples and dicts). Prefer **f-strings**, **`str.format()`**, or **`string.Template`** for new code.

The **`%`** operator performs **printf-style interpolation**: `format % values` replaces conversion specifications in `format`, similar to C `sprintf`.

```python
assert '%s has %d quote types.' % ('Python', 2) == 'Python has 2 quote types.'
assert '%(language)s has %(number)03d quote types.' % {'language': 'Python', 'number': 2} == 'Python has 002 quote types.'
```

- **Single argument:** `values` may be a non-tuple object when the format expects one conversion.
- **Multiple arguments:** `values` must be a **tuple** with exactly the right length, or a **mapping** when using `%(name)s` keys (no `*` width/precision from mapping).

A conversion specifier has, in order: `%`, optional `(name)`, flags, width, precision, ignored length modifier, and **conversion type**.

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
| `u` | Obsolete; same as `d`. | (6) |
| `x` | Signed hex (lowercase). | (2) alternate: `0x`. |
| `X` | Signed hex (uppercase). | (2) alternate: `0X`. |
| `e` | Float, exponential (lowercase). | (3) |
| `E` | Float, exponential (uppercase). | (3) |
| `f` | Float, decimal format. | (3) |
| `F` | Float, decimal format. | (3) |
| `g` | Float; uses `%e` or `%f` style by magnitude. | (4) |
| `G` | Like `g` but uppercase exponent. | (4) |
| `c` | Single character (int or length-1 str). | |
| `r` | String via `repr()`. | (5) |
| `s` | String via `str()`. | (5) |
| `a` | String via `ascii()`. | (5) |
| `%` | Literal `%` in the result. | |

**Notes:** (1) octal alternate form; (2) hex alternate `0x`/`0X`; (3) precision defaults to 6 fractional digits; (4) `%g`/`%G` precision counts significant digits; (5) no NUL (`\0`) termination for `%s`; (6) `%u` is obsolete. See [PEP 237](https://peps.python.org/pep-0237/) for integer display rules.

> **Changed in version 3.1:** `%f` for very large magnitudes is no longer silently switched to `%g`.

Since Python `str` has an explicit length, `%s` does **not** treat `\0` as end-of-string.

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Common Sequence Operations](../sequence-types-list-tuple-range/common-sequence-operations/index.md) | Indexing, slicing, and `in` shared by `str`, `list`, `tuple`, and others. |
| [Binary Sequence Types — bytes, bytearray, memoryview](../binary-sequence-types-bytes-bytearray-memoryview/index.md) | Bytes-like objects, decoding, and the buffer protocol paired with `str.encode()`. |
