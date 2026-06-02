# [Formal grammar for f-strings](https://docs.python.org/3/reference/lexical_analysis.html#formal-grammar-for-f-strings)

F-strings provide a concise way to embed expressions inside string literals, using the `{}` curly braces notation. Parsing and evaluating f-strings is handled in two steps in the Python interpreter:

- **Lexical analysis**: Breaks f-strings into tokens like `FSTRING_START`, `FSTRING_MIDDLE`, and `FSTRING_END`.
- **Parsing**: Handles any Python expressions found within the curly braces.

> **Note:** The precise breakdown between the lexer and the parser is an implementation detail in CPython and could differ across interpreters. Generally, expressions inside `{}` are not evaluated during tokenization, but passed to the parser for evaluation.

---

## Whitespace Rules

Whitespace has special significance at certain parts of an f-string:

- **No Whitespace in Start:** There must be no whitespace between the prefix (`f`, `fr`, etc.) and the opening quote.

  **Correct:**
  ```python
  f"hello"
  fr'world'
  ```

  **Incorrect:**
  ```python
  f "hello"   # SyntaxError: unexpected space
  ```

- **Whitespace in Middle:** Any whitespace in the middle of the string is treated as part of the string literal.

  **Example:**
  ```python
  name = "Alice"
  greeting = f"Hello,   {name}!"   # The spaces are preserved
  print(greeting)   # Output: Hello,   Alice!
  ```

- **Whitespace After Debug Specifier:** If you use the debug specifier (`=`) in a replacement field, all whitespace after the opening brace up to the `=` (and right after the `=`) is preserved as part of the evaluated expression.

  **Example:**
  ```python
  x = 10
  print(f"{   x   = }")   # Output: x   = 10
  ```

---

## Grammar Summary (with Explanations)

Below is a summary of the formal grammar for f-strings, supplemented by real-world examples.

```ebnf
fstring:    FSTRING_START fstring_middle* FSTRING_END

FSTRING_START:      fstringprefix ("'" | '"' | "'''" | '"""')
FSTRING_END:        f_quote
fstringprefix:      <("f" | "fr" | "rf"), case-insensitive>
f_debug_specifier:  '='
f_quote:            <the quote character(s) used in FSTRING_START>

fstring_middle:
   | fstring_replacement_field
   | FSTRING_MIDDLE

FSTRING_MIDDLE:
   | (!'\' !newline !'{' !'}' !f_quote) source_character
   | stringescapeseq
   | "{{"
   | "}}"
   | <newline, in triple-quoted f-strings only>

fstring_replacement_field:
   | '{' f_expression [f_debug_specifier] [fstring_conversion] [fstring_full_format_spec] '}'

fstring_conversion:
   | "!" ("s" | "r" | "a")

fstring_full_format_spec:
   | ':' fstring_format_spec*

fstring_format_spec:
   | FSTRING_MIDDLE
   | fstring_replacement_field

f_expression:
   | ','.(conditional_expression | "*" or_expr)+ [","]
   | yield_expression
```

- **Token Explanations:**
  - `FSTRING_START` and `FSTRING_END` delimit the start and end of the f-string, just as quotes do for regular strings.
  - `fstring_middle` is either more string content or a replacement field.
  - `fstring_replacement_field` is evaluated, returning a string representation of the result.
  - `f_debug_specifier` introduces a debugging display.

### **Examples**

#### 1. Basic Replacement Field

```python
name = "Alice"
age = 30
greeting = f"Hello, {name}. You are {age}."
print(greeting)  # Output: Hello, Alice. You are 30.
```

#### 2. Using the Debug Specifier

```python
value = 42
print(f"{value = }")  # Output: value = 42
```

#### 3. String Conversion Flags

```python
word = "Hello\nWorld"
print(f"{word!r}")  # Output: 'Hello\nWorld'
print(f"{word!s}")  # Output: Hello
                   #         World
print(f"{word!a}")  # Output: 'Hello\\nWorld'
```

#### 4. Formatting Inside Replacement Fields

```python
pi = 3.14159
print(f"{pi:.2f}")  # Output: 3.14
```

#### 5. Nested Replacement Fields

You can use nested fields for formatting:

```python
name = "Alice"
width = 10
print(f"{name:{width}}")  # Output: 'Alice     '
```

#### 6. Escaping Braces

To include a literal brace, double it:

```python
print(f"Use brackets like {{ and }}")  # Output: Use brackets like { and }
```

#### 7. Triple-Quoted f-Strings

Triple quotes allow multi-line f-strings:

```python
user = "Bob"
msg = f"""Dear {user},

Welcome to the program!

Regards,
Team"""
print(msg)
```

---

**Note:** In the above grammar, `f_quote` and `FSTRING_MIDDLE` are context sensitive—they depend on which quote character started the string, and the source content.

---

## t-String Grammar

`t`-strings (introduced in Python 3.14) follow the *exact* formal grammar as f-strings, except all rule and token names use a `t` instead of `f`, and the prefix is `t` (or `tr`, etc.) rather than `f`.

**Example:**

```python
from string import Template

user = "Charlie"
tpl = t"Hello, $user"
print(tpl.substitute(user=user))  # Output: Hello, Charlie
```

> For details, see the [t-strings section](../t-strings/index.md).