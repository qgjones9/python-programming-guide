# [Text](https://docs.python.org/3/tutorial/introduction.html#text)

Python can manipulate **text**—characters, words, sentences, and symbols—as well as numbers. Text values have type [`str`](../../../../standard-library/built-in-types/text-sequence-type-str/index.md) (commonly called **strings**). Examples include `"!"`, `"rabbit"`, `"Paris"`, and `"Got your back."`.

## String literals

A **string literal** is text written directly in your code inside quotation marks. Single quotes (`'...'`) and double quotes (`"..."`) work the same way; choose whichever makes quoting easier.

```shell
>>> 'spam eggs'  # single quotes
'spam eggs'
>>> "Paris rabbit got your back :)! Yay!"  # double quotes
'Paris rabbit got your back :)! Yay!'
>>> '1975'  # digits in quotes are strings, not numbers
'1975'
```

Unlike some other languages, escape sequences such as `\n` behave the same in both quote styles. The only practical difference is which inner quote character you must escape.

## Escaping quotes

To include a quote character inside a string, **escape** it with a backslash (`\`), or wrap the literal in the other kind of quotes.

```shell
>>> 'doesn\'t'  # escape the single quote
"doesn't"
>>> "doesn't"  # or use double quotes instead
"doesn't"
>>> '"Yes," they said.'
'"Yes," they said.'
>>> "\"Yes,\" they said."
'"Yes," they said.'
>>> '"Isn\'t," they said.'
'"Isn\'t," they said.'
```

## Display in the REPL vs [`print()`](../../../../standard-library/built-in-functions/print/index.md)

In the interactive shell, typing a string expression shows its **repr**—including the surrounding quotes and visible escape characters. The [`print()`](../../../../standard-library/built-in-functions/print/index.md) function produces **human-readable** output: no extra quotes, and escape sequences like `\n` are interpreted.

```shell
>>> s = 'First line.\nSecond line.'  # \n means newline
>>> s  # without print(), escapes appear literally in the display
'First line.\nSecond line.'
>>> print(s)  # print() interprets \n as a line break
First line.
Second line.
```

## Raw strings

When you do **not** want backslash escapes processed, prefix the opening quote with `r` to create a **raw string**. This is handy for Windows paths and regular-expression patterns.

```shell
>>> print('C:\this\name')  # \t is tab, \n is newline
C:	his
ame
>>> print(r'C:\this\name')  # note the r before the quote
C:\this\name
```

There is one subtle rule: a raw string literal may not end with an odd number of `\` characters. See the [official FAQ entry](https://docs.python.org/3/faq/design.html#why-can-t-raw-strings-r-strings-end-with-a-backslash) for workarounds.

## Multi-line string literals

String literals can span multiple lines using **triple quotes**: `"""..."""` or `'''...'''`. End-of-line characters become part of the string. Add `\` at the end of a line to join lines without inserting a newline; the example below omits the initial blank line.

```shell
>>> print("""\
... Usage: thingy [OPTIONS]
...      -h                        Display this usage message
...      -H hostname               Hostname to connect to
... """)
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
```

## Concatenation and repetition

Use `+` to **concatenate** (join) strings and `*` to **repeat** a string a given number of times.

```shell
>>> # 3 times 'un', followed by 'ium'
>>> 3 * 'un' + 'ium'
'unununium'
```

## Implicit literal concatenation

Two or more **string literals** placed next to each other are automatically concatenated at compile time. This is useful for breaking long literals across lines.

```shell
>>> 'Py' 'thon'
'Python'
>>> text = ('Put several strings within parentheses '
...         'to have them joined together.')
>>> text
'Put several strings within parentheses to have them joined together.'
```

This only works for **literals**, not for variables or expressions:

```shell
>>> prefix = 'Py'
>>> prefix 'thon'  # can't concatenate a variable and a string literal
  File "<stdin>", line 1
    prefix 'thon'
           ^^^^^^
SyntaxError: invalid syntax
>>> ('un' * 3) 'ium'
  File "<stdin>", line 1
    ('un' * 3) 'ium'
               ^^^^^
SyntaxError: invalid syntax
```

To join variables or mix variables with literals, use `+`:

```shell
>>> prefix + 'thon'
'Python'
```

## Indexing

Strings are **sequences**: you can access individual characters with **indexing** (subscripting). The first character is at index `0`. Python has no separate character type—a single character is simply a string of length one.

```shell
>>> word = 'Python'
>>> word[0]  # character in position 0
'P'
>>> word[5]  # character in position 5
'n'
```

## Negative indices

**Negative indices** count from the end of the string. The last character is at index `-1`. Because `-0` is the same as `0`, there is no “negative zero” index—counting backward starts at `-1`.

```shell
>>> word[-1]  # last character
'n'
>>> word[-2]  # second-last character
'o'
>>> word[-6]
'P'
```

## Slicing

**Slicing** extracts a substring using `start:stop` notation. The start index is **included**; the stop index is **excluded**.

```shell
>>> word[0:2]  # characters from position 0 (included) to 2 (excluded)
'Py'
>>> word[2:5]  # characters from position 2 (included) to 5 (excluded)
'tho'
```

Omitted indices use useful defaults: a missing start means “from the beginning”; a missing stop means “through the end.”

```shell
>>> word[:2]   # from the beginning to position 2 (excluded)
'Py'
>>> word[4:]   # from position 4 (included) to the end
'on'
>>> word[-2:]  # from the second-last (included) to the end
'on'
```

Because the end index is always excluded, `s[:i] + s[i:]` always reconstructs the full string:

```shell
>>> word[:2] + word[2:]
'Python'
>>> word[:4] + word[4:]
'Python'
```

### How slice indices line up

Think of indices as pointing **between** characters, not at them. For a string of length *n*, valid positions run from `0` through `n` (the position after the last character):

```text
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
 0   1   2   3   4   5   6
-6  -5  -4  -3  -2  -1
```

The top row shows non-negative indices; the bottom row shows the corresponding negative indices. A slice from *i* to *j* includes every character between those boundary markers.

For non-negative indices within bounds, the length of `word[i:j]` is `j - i`. For example, `word[1:3]` has length `2`.

## Out-of-range indexes

An index that is too large raises `IndexError`. Out-of-range **slice** bounds are handled gracefully—they clip to the string edges instead of failing.

```shell
>>> word[42]  # the word only has 6 characters
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: string index out of range
>>> word[4:42]
'on'
>>> word[42:]
''
```

## Immutability

Python strings are **immutable**: you cannot change characters in place. Assigning to an indexed position raises `TypeError`.

```shell
>>> word[0] = 'J'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
>>> word[2:] = 'py'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
```

To “change” a string, build a **new** string from pieces:

```shell
>>> 'J' + word[1:]
'Jython'
>>> word[:2] + 'py'
'Pypy'
```

## Length with [`len()`](../../../../standard-library/built-in-functions/len/index.md)

The built-in [`len()`](../../../../standard-library/built-in-functions/len/index.md) function returns the number of characters in a string.

```shell
>>> s = 'supercalifragilisticexpialidocious'
>>> len(s)
34
```

## See also

| Topic | Notes |
|-------|-------|
| [Text Sequence Type — str](../../../../standard-library/built-in-types/text-sequence-type-str/index.md) | Strings are **sequence types** and support common sequence operations. |
| [String methods](https://docs.python.org/3/library/stdtypes.html#string-methods) | Built-in methods for searching, splitting, and transforming text. |
| [Formatted string literals](../../../../language-reference/lexical-analysis/string-and-bytes-literals/f-strings/index.md) | **f-strings** embed expressions inside string literals. |
| [The string format method](../../../../tutorial/input-and-output/fancier-output-formatting/the-string-format-method/index.md) | Format strings with [`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format). |
| [Old string formatting](../../../../tutorial/input-and-output/fancier-output-formatting/old-string-formatting/index.md) | **printf-style** formatting with the `%` operator. |
