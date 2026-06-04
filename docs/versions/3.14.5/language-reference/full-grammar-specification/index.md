# [10. Full Grammar specification](https://docs.python.org/3/reference/grammar.html)

Chapter 10 is the **complete PEG grammar** for Python, derived from the grammar that generates the CPython parser (`Grammar/python.gram` in the CPython source). The official page is the authoritative syntax definition; this mirror summarizes how to read it and how it relates to earlier chapters.

Unlike lexical rules in [Lexical analysis](../lexical-analysis/index.md), this grammar consumes **tokens** (`NAME`, `NUMBER`, `NEWLINE`, `INDENT`, …), not individual characters.

## Notation recap

The grammar uses the same notation as [Notation](../introduction/notation/index.md), plus one extra symbol:

| Symbol | Meaning |
|--------|---------|
| `~` (cut) | Commit to the current alternative; if parsing fails after the cut, the whole rule fails without trying other alternatives |

Cuts optimize parsing and improve error messages. They rarely change what programs are valid; behavior inside parentheses or lookaheads is deliberately unspecified.

Other PEG features in this grammar:

| Form | Meaning |
|------|---------|
| `e1 e2` | Sequence |
| `e1 \| e2` | Ordered choice (first match wins) |
| `( e )`, `[ e ]`, `e*`, `e+` | Grouping, optional, repetition |
| `&e` / `!e` | Positive / negative lookahead |
| `s.e+` | One or more `e` separated by `s` (separator not in parse tree) |
| `'if'` / `"match"` | Keyword / soft keyword |
| `NAME` | Token from the lexer |

Rules named `invalid_*` are used only on a **second parse pass** for specialized syntax errors after the first pass fails.

## Starting rules

The grammar defines several entry points for different parsing modes:

| Rule | Input accepted |
|------|----------------|
| `file` | Module: optional `statements`, then `ENDMARKER` |
| `interactive` | REPL: one `statement_newline` |
| `eval` | `eval()`: `expressions`, optional newlines, `ENDMARKER` |
| `func_type` | String passed to `typing.get_type_hints` for forward references |

```python
import ast

# file starting rule: a module body parses as a Module node.
tree = ast.parse("x = 1\n")
assert isinstance(tree, ast.Module)

# eval starting rule: a single expression.
expr = ast.parse("1 + 2", mode="eval")
assert isinstance(expr, ast.Expression)

# single starting rule: one statement (REPL / ast.parse mode="single").
stmt = ast.parse("pass\n", mode="single")
assert isinstance(stmt.body[0], ast.Pass)
```

## Top-level structure

At the highest level, statements split into **simple** and **compound** forms—the same split documented in [Simple statements](../simple-statements/index.md) and [Compound statements](../compound-statements/index.md):

```ebnf
statements: statement+
statement: compound_stmt | simple_stmts
```

**Important ordering note:** in `simple_stmt`, `assignment` must appear **before** `star_expressions`. Otherwise a simple assignment like `x = 1` would be parsed as an expression statement and then rejected.

```python
import ast

# Valid assignment parses cleanly.
ast.parse("total = count + 1")

# Expression-statement form without assignment.
ast.parse("count + 1")

# Augmented assignment is a distinct simple_stmt alternative.
ast.parse("count += 1")
```

## Major rule groups

The full grammar on docs.python.org is organized in comment blocks. Use these local chapters when reading the corresponding rules:

| Grammar block | Language Reference chapter |
|---------------|----------------------------|
| `simple_stmt`, `import_stmt`, … | [Simple statements](../simple-statements/index.md) |
| `compound_stmt`, `function_def`, `class_def`, … | [Compound statements](../compound-statements/index.md) |
| `named_expression`, `expression`, operators | [Expressions](../expressions/index.md) |
| Token names (`NAME`, `STRING`, …) | [Lexical analysis](../lexical-analysis/index.md) |

## Reading a rule in practice

1. Find the **starting rule** for your context (`file`, `eval`, etc.).
2. Expand **non-terminals** by name; token names refer to lexer output.
3. Respect **ordered choice**: earlier alternatives in a `|` list take precedence.
4. Watch for **`~` cuts** and **`invalid_*` rules**—they affect error reporting, not usually valid programs.
5. Cross-check semantics in the narrative chapters; the grammar alone does not define evaluation order or name binding.

```python
import ast

source = """
def greet(name: str) -> str:
    return f"Hello, {name}!"
"""
tree = ast.parse(source)
func = tree.body[0]
assert func.name == "greet"
assert len(func.args.args) == 1
assert isinstance(func.body[0], ast.Return)
```

For the machine-readable grammar text and every production rule, use the canonical page: [10. Full Grammar specification](https://docs.python.org/3/reference/grammar.html).

Parent: [The Python Language Reference](../index.md)
