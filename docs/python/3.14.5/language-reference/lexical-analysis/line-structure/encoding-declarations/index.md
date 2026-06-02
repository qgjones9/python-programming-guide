# [Encoding declarations](https://docs.python.org/3/reference/lexical_analysis.html#encoding-declarations)

In Python, you can specify the encoding of your source file by adding a special comment at the top—on either the first or second line of your script. This is called an *encoding declaration*. Python will look for a comment that matches the format `coding[=:]\s*([-\w.]+)`, where the value in parentheses (like `utf-8`) tells Python what encoding to use.

Here’s how to write an encoding declaration:

- Place the encoding comment on its own line, by itself.
- If you put it on the second line, the first line must also be a comment (for example, with a shebang or another comment).

The two most popular ways to declare the encoding are:

```python
# -*- coding: <encoding-name> -*-
```

This format is also recognized by GNU Emacs editors.

Or:

```python
# vim:fileencoding=<encoding-name>
```
This format works in the VIM editor.

If you do not specify an encoding, Python assumes the file uses `UTF-8` encoding by default. Also, when using UTF-8 (explicitly or by default), a UTF-8 byte order mark at the start of the file (`b'\xef\xbb\xbf'`) will be ignored and won’t cause a syntax error.

If you do provide an encoding declaration, the encoding name must be one that Python recognizes (see the official list in [Python’s Standard Encodings documentation](../../../../standard-library/binary-data-services/codecs-codec-registry-and-base-classes/standard-encodings/index.md)). Python uses the chosen encoding for all aspects of lexical analysis—meaning it affects how string literals, comments, and identifiers are interpreted as text.

Python reads your source code by first converting it into Unicode text, using the encoding you specified (or UTF-8 by default). This means your code—everything from variable names to string literals—can include any Unicode character (like letters from any language or special symbols), except for the NUL character (which represents "zero" in C and binary files and isn’t allowed in source files).

So, in simple terms: as long as you’re not using the NUL byte, you can write Python code using almost any character from the entire Unicode set. For example, identifiers (like variable names), comments, and string contents can all contain non-ASCII characters.

```ebnf
source_character:  <any Unicode code point, except NUL>
```

```python
# This is a comment with a non-ASCII character: é
print("Hello, World!")  # This is also a comment with a non-ASCII character: é
print("こんにちは")  # This is a string with a non-ASCII character: こんにちは
```

