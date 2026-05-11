# [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html)

Condensed notes for [chapter 3 of the Python Tutorial](https://docs.python.org/3/tutorial/introduction.html). For full prose, examples, and updates, follow the heading link.

### Reading the examples

- **`>>>` / `...`** mark input vs output; a lone `...` line means type a blank line to finish a block.
- **`#` starts a comment** to the end of the line (not inside string literals).
- The docs’ **Copy** control strips prompts so you can paste into the interpreter.

```python
# Comments run to the end of the line.
spam = 1  # and can follow code
text = "# This is not a comment — it is inside a string."
```

### 3.1 — Using Python as a calculator

- **Numbers:** `+ - * /`, parentheses; **`/` always returns a float**; use **`//`** for floor division and **`%`** for remainder; **`**`** for powers.
- **Assignment** with `=`; using an undefined name raises **`NameError`**.
- **Mixed int/float** arithmetic promotes to float.
- In interactive mode, **`_`** holds the last printed expression (treat as read-only).
- Other numeric types exist (**`Decimal`**, **`Fraction`**, **`complex`** with `j`/`J`).

```python
# Basic arithmetic; `/` returns float
assert (50 - 5 * 6) / 4 == 5.0
assert 8 / 5 == 1.6

assert 17 // 3 == 5  # floor division
assert 17 % 3 == 2  # remainder
assert 5**2 == 25 and 2**7 == 128

width, height = 20, 5 * 9
assert width * height == 900

try:
    eval("__not_a_real_name__", {})
except NameError:
    pass

assert 4 * 3.75 - 1 == 14.0  # int promoted to float in mixed expressions

# In the REPL only: after an expression prints, `_` holds that value.
# In a .py file, `_` is an ordinary identifier — do not rely on “last result” magic.

from decimal import Decimal
from fractions import Fraction

assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
assert Fraction(2, 3) + Fraction(1, 6) == Fraction(5, 6)
assert (1 + 2j).imag == 2
```

### 3.1.2 — Text (strings)

- **`str`**: single (`'...'`) or double (`"..."`) quotes; escape with **`\`** or use the other quote style.
- **`print()`** shows human-readable output; showing a value at the prompt may still show quotes/escapes.
- **Raw strings** `r'...'` avoid most escape interpretation (with a caveat about trailing `\`).
- **Triple-quoted** strings can span lines; a `\` at end of line can drop an unwanted leading newline.
- **Concatenation** `+`, repetition `*`; **adjacent string literals** concatenate automatically (not variables).
- **Indexing and slicing** (`word[0]`, `word[0:2]`, defaults, negative indices); out-of-range index errors vs forgiving slices.
- **Strings are immutable** (no item assignment); build new strings instead.
- **`len()`** for length.

```python
assert "spam" + " eggs" == "spam eggs"
assert 3 * "un" + "ium" == "unununium"
assert "Py" "thon" == "Python"  # adjacent literals only; not variables

word = "Python"
assert word[0] == "P" and word[-1] == "n"
assert word[0:2] == "Py" and word[2:5] == "tho"
assert word[:2] + word[2:] == word

s = "First line.\nSecond line."
assert "\n" in s  # real newline in the value
assert "\\n" in repr(s)  # repr shows it as an escape sequence
print(s)  # newline rendered when printed

assert r"C:\this\name" == "C:\\this\\name"  # raw string: fewer surprises with backslashes

usage = """\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
"""
assert usage.startswith("Usage:")

prefix = "Py"
assert prefix + "thon" == "Python"

# Immutability: assign by building a new string
assert "J" + word[1:] == "Jython"

assert len("supercalifragilisticexpialidocious") == 34
```

### 3.1.3 — Lists

- **Comma-separated values in `[...]`**; often homogeneous types.
- Like strings: **indexing and slicing**; unlike strings: **mutable** (assign to indices, **`append()`**, slice assignment can resize or clear).
- Assignment **binds names to the same list** (shared references); **slicing** like `[:]` can give a **shallow copy**.
- Lists can be **nested**; **`len()`** applies.

```python
squares = [1, 4, 9, 16, 25]
assert squares[0] == 1 and squares[-3:] == [9, 16, 25]

cubes = [1, 8, 27, 65, 125]
cubes[3] = 64  # in-place mutation
cubes.append(216)

rgb = ["Red", "Green", "Blue"]
rgba = rgb
rgba.append("Alph")
assert rgb[-1] == "Alph"  # same object

copy = rgba[:]
copy[-1] = "Alpha"
assert rgba[-1] == "Alph" and copy[-1] == "Alpha"

letters = ["a", "b", "c", "d", "e", "f", "g"]
letters[2:5] = ["C", "D", "E"]
letters[2:5] = []
letters[:] = []
assert letters == [] and len(letters) == 0

nested = [["a", "b", "c"], [1, 2, 3]]
assert nested[0][1] == "b"
```

### 3.2 — First steps toward programming

- Example uses **`while`**, **`print()`**, and a **Fibonacci** loop.
- **Multiple assignment** (`a, b = 0, 1`) and the rule that **right-hand sides are evaluated before** assignments.
- **Truthiness** in conditions: non-zero numbers, non-empty sequences, etc.
- **Indentation** defines the loop body; at the REPL, end a compound statement with a **blank line**.
- **`print()`** formatting (e.g. multiple values, **`end=`**).

```python
from io import StringIO

# Fibonacci: while + multiple assignment
a, b = 0, 1
out = []
while a < 10:
    out.append(a)
    a, b = b, a + b
assert out == [0, 1, 1, 2, 3, 5, 8]

# Truthiness: empty list is falsey
items = []
if not items:
    items.append("ready")

# print with several values and custom end (capture instead of REPL)
buf = StringIO()
i = 256 * 256
print("The value of i is", i, file=buf)
assert "65536" in buf.getvalue()

buf = StringIO()
a, b = 0, 1
while a < 1000:
    print(a, end=",", file=buf)
    a, b = b, a + b
assert buf.getvalue().startswith("0,1,1,2,")
```

### Footnotes (called out on the page)

- **`**` binds tighter than unary `-`** (e.g. `-3**2` is `-9`; use **`(-3)**2`** for `9`).
- **Escape rules** are the same in single- and double-quoted strings; only which quote must be escaped changes.

```python
assert -3**2 == -(3**2) == -9
assert (-3) ** 2 == 9

# Same escapes in '...' vs "..."; choose quotes to minimize escaping
assert 'doesn\'t' == "doesn't"
assert "\"Yes,\" they said." == '"Yes," they said.'
```

## Sections in this repo

- [Using Python as a Calculator](using-python-as-a-calculator/index.md) — [Numbers](using-python-as-a-calculator/numbers/index.md), [Text](using-python-as-a-calculator/text/index.md), [Lists](using-python-as-a-calculator/lists/index.md)
- [First Steps Towards Programming](first-steps-towards-programming/index.md)


Next: [More Control Flow Tools](../more-control-flow-tools/index.md)