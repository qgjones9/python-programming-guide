# [2.7. Operators and delimiters](https://docs.python.org/3/reference/lexical_analysis.html#operators-and-delimiters)

Besides names, literals, and line-structure tokens, Python source is built from punctuation: symbols such as `+`, `==`, `(`, and `,`. During lexical analysis, most of these become a single [`OP`](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#core-tokens-names-literals-and-generic-operators) token—the generic type for **operators** (symbols that combine or transform expressions) and **delimiters** (symbols that structure or separate other tokens).

The grammar below lists every symbol that can appear as `OP`. For the corresponding `token.PLUS`, `token.LPAR`, and other **exact** constants, see [Operators and delimiters (exact types)](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#operators-and-delimiters-exact-types) in the `token` module documentation.

## Formal grammar

The lexer recognizes one `OP` token per match. The top-level rule groups symbols by role:

```ebnf
OP:
   | assignment_operator
   | bitwise_operator
   | comparison_operator
   | enclosing_delimiter
   | other_delimiter
   | arithmetic_operator
   | "..."
   | other_op
```

Each category is defined as follows:

```ebnf
assignment_operator:
   "+=" | "-=" | "*=" | "**=" | "/=" | "//=" | "%="
 | "&=" | "|=" | "^=" | "<<=" | ">>=" | "@=" | ":="

bitwise_operator:
   "&" | "|" | "^" | "~" | "<<" | ">>"

comparison_operator:
   "<=" | ">=" | "<" | ">" | "==" | "!="

enclosing_delimiter:
   "(" | ")" | "[" | "]" | "{" | "}"

other_delimiter:
   "," | ":" | "!" | ";" | "=" | "->"

arithmetic_operator:
   "+" | "-" | "**" | "*" | "//" | "/" | "%"

other_op:
   "." | "@"
```

## Quick reference by category

| Category | Symbols | Typical use |
|----------|---------|-------------|
| **Assignment** | `+=`, `-=`, `*=`, …, `:=` | In-place updates; walrus binding |
| **Arithmetic** | `+`, `-`, `*`, `/`, `//`, `%`, `**` | Numeric operations |
| **Bitwise** | `&` `|` `^` `~` `<<` `>>` | Integer bit operations |
| **Comparison** | `<`, `>`, `<=`, `>=`, `==`, `!=` | Ordering and equality tests |
| **Enclosing** | `( )`, `[ ]`, `{ }` | Grouping, calls, collections, blocks |
| **Other delimiter** | `,`, `:`, `!`, `;`, `=`, `->` | Separators, slices, annotations, conversion in f-strings |
| **Other op** | `.`, `@` | Attribute access; matrix multiply / decorators |
| **Ellipsis** | `...` | The [`Ellipsis`](../../../standard-library/built-in-types/other-built-in-types/index.md) literal |

## Operators vs delimiters

**Operators** usually sit *between* expressions and denote an operation (`a + b`, `x == y`). **Delimiters** usually *structure* code—parentheses, brackets, commas, colons—without combining arbitrary operands on their own.

Python’s reference grammar uses the names above for documentation, but there is **no strict formal line** between “operator” and “delimiter.” The same character can play different roles depending on context.

## Symbols with more than one role

Some `OP` tokens mean one thing in an expression and another in grammar or unpacking:

| Symbol | As operator | As delimiter or other role |
|--------|-------------|----------------------------|
| `*` | Multiplication (`a * b`) | Iterable unpacking (`*args`, `**kwargs`) |
| `@` | Matrix multiplication (`a @ b`) | Decorator prefix (`@staticmethod`) |
| `+` / `-` | Addition / subtraction | Unary plus / minus on a literal (see [Numeric literals](../numeric-literals/index.md)) |
| `:` | — | Slices, blocks, type annotations, f-string conversion (`!s`) |
| `=` | — | Keyword arguments, defaults (`def f(x=1)`) — distinct from `==` |

```python
# * as operator vs unpacking
area = 3 * 4
def greet(*names):
    print(', '.join(names))

# @ as matrix multiply vs decorator
import numpy as np
C = A @ B

@classmethod
def create(cls):
    return cls()
```

For `.`, `(`, and `)`, textbooks disagree: some call them delimiters around calls and attribute access; others describe `.` as the attribute operator and `()` as the call operator. At the token level they are all `OP`; the parser assigns meaning from position.

## Keyword operators

Not every operator is an `OP` token. Boolean logic and some membership tests use **keywords** instead of punctuation:

```python
if x and y or not z:
    ...

if item in collection:
    ...
```

Those words are [`NAME`](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#core-tokens-names-literals-and-generic-operators) tokens reserved as keywords, not symbol operators. See [Names (identifiers and keywords)](../names-identifiers-and-keywords/index.md).

## The `...` (Ellipsis) token

Three consecutive periods form a single token in the `OP` rule. At runtime they denote the singleton **`Ellipsis`** object—often used as a placeholder in stubs or slicing:

```python
def todo():
    ...   # same as Ellipsis; common in stub files

data = [1, 2, 3, 4, 5]
data[...]   # full slice via Ellipsis (uncommon in everyday code)
```

It must be exactly three period characters with no spaces between them.

## Related sections

| Section | Description |
|---------|-------------|
| [Other tokens](../other-tokens/index.md) | How `OP` fits with `NAME`, `NUMBER`, and `STRING` |
| [token module (exact types)](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#operators-and-delimiters-exact-types) | `token.PLUS`, `token.LPAR`, and every specific constant |
| [Literals](../literals/index.md) | String, bytes, numeric, and special literals including `...` |
| [Numeric literals](../numeric-literals/index.md) | Unary `+` and `-` before number tokens |
