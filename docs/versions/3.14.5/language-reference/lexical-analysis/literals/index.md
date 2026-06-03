# [2.4. Literals](https://docs.python.org/3/reference/lexical_analysis.html#literals)

A **literal** in Python is a notation that directly represents a fixed value in source code. Literals provide explicit values for built-in data types during lexical analysis (the process by which code is broken into tokens). Python recognizes several main kinds of literals:

- **String literals:** Sequences of text, enclosed in single quotes (`'...'`) or double quotes (`"..."`).  
  For example:
  ```python
  "spam"
  'eggs'
  ```
  - The type of quote used to open the string must also be used to close it. This means you can include the *other* type of quote inside the string without escaping, useful for sentences like:
    ```python
    'Say "Hello", please.'
    "Don't do that!"
    ```
  - **Escape sequences:** The backslash (`\`) introduces an escape sequence, which signals a special character or behavior. For example, `\"` represents a literal double quote within a double-quoted string, so it isn't treated as the end of the string.
    ```python
    print("Say \"Hello\" to everyone!")
    # Output: Say "Hello" to everyone!
    ```
  See below for a full list of escape sequences.

- **Bytes literals:** Like string literals, but prefixed with `b` or `B`, these represent sequences of bytes rather than Unicode text.

- **Numeric literals:** Direct representations of numbers such as integers and floating-point values (e.g., `42`, `3.14`, `0b1010`).

- **Special value literals:** Some constant values are introduced by keywords—`None`, `True`, `False`—and the ellipsis literal, `...`, which is a single token.

Each type of literal provides a concise and unambiguous way to represent core data values in Python code.