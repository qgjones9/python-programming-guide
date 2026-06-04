# [ast — Abstract syntax trees](https://docs.python.org/3/library/ast.html)

The [`ast`](https://docs.python.org/3/library/ast.html) module defines the node types Python's parser builds from source and provides utilities to **parse**, **walk**, **transform**, and **unparse** those trees. It is the foundation for linters, formatters, macro systems, and static analysis. Full node reference and edge cases remain on [docs.python.org](https://docs.python.org/3/library/ast.html).

Related: [`tokenize`](../tokenize-tokenizer-for-python-source/index.md) for lexical tokens, [`symtable`](../symtable-access-to-the-compilers-symbol-tables/index.md) for scope tables, and [`compile`](../../built-in-functions-and-types/compile/index.md) to turn an AST back into executable code.

---

## Core functions — [Node classes](https://docs.python.org/3/library/ast.html#node-classes)

| Function / class | Role |
|------------------|------|
| `ast.parse(source, mode='exec', ...)` | Build a `Module`, `Expression`, or `Interactive` root from source |
| `ast.literal_eval(node_or_string)` | Safely evaluate constant literals only |
| `ast.unparse(node)` | Render an AST back to source text (3.9+) |
| `ast.walk(tree)` | Depth-first yield of all nodes |
| `ast.iter_fields(node)` | `(name, value)` pairs on a node |
| `ast.get_source_segment(source, node)` | Extract original source span for a node |
| `ast.fix_missing_locations(tree)` | Fill `lineno` / `col_offset` for generated nodes |

```python
# Goal: parse and inspect a function definition
import ast

source = "def greet(name):\n    return f'hi {name}'\n"
tree = ast.parse(source)
func = tree.body[0]
assert isinstance(func, ast.FunctionDef)
assert func.name == "greet"
assert len(func.args.args) == 1
```

```python
# Goal: literal_eval rejects non-constant expressions
import ast

assert ast.literal_eval("[1, 2, {'a': 3}]") == [1, 2, {"a": 3}]
try:
    ast.literal_eval("1 + 2")
except ValueError:
    pass
else:
    raise AssertionError("expected ValueError for non-literal")
```

---

## Walking and transforming — [ast.NodeVisitor](https://docs.python.org/3/library/ast.html#ast.NodeVisitor)

| Pattern | Use when |
|---------|----------|
| Subclass `ast.NodeVisitor` | Read-only traversal; override `visit_<NodeType>` |
| Subclass `ast.NodeTransformer` | Return modified nodes to rewrite the tree |
| `ast.copy_location(new, old)` | Preserve line numbers after generating nodes |

```python
# Goal: count function definitions with NodeVisitor
import ast

class FuncCounter(ast.NodeVisitor):
    def __init__(self):
        self.count = 0

    def visit_FunctionDef(self, node):
        self.count += 1
        self.generic_visit(node)

source = "def a(): pass\ndef b(): pass\nclass C:\n    def m(self): pass\n"
counter = FuncCounter()
counter.visit(ast.parse(source))
assert counter.count == 3
```

```python
# Goal: rename a name with NodeTransformer
import ast

class Renamer(ast.NodeTransformer):
    def __init__(self, old, new):
        self.old, self.new = old, new

    def visit_Name(self, node):
        if node.id == self.old:
            return ast.copy_location(ast.Name(id=self.new, ctx=node.ctx), node)
        return node

tree = ast.parse("x = 1\nprint(x)\n")
Renamer("x", "value").visit(tree)
assert ast.unparse(tree).strip() == "value = 1\nprint(value)"
```

---

## `mode` and `feature_version`

| `mode` | Root node type | Typical use |
|--------|----------------|-------------|
| `'exec'` | `ast.Module` | Scripts and modules |
| `'eval'` | `ast.Expression` | Single expression (`compile` + eval) |
| `'single'` | `ast.Interactive` | REPL input |

Pass **`feature_version=(major, minor)`** when parsing code meant for an older grammar (for example pre-3.7 `async`/`await` rules).

```python
# Goal: parse an expression for eval-style compilation
import ast

node = ast.parse("2 ** 8", mode="eval")
assert isinstance(node, ast.Expression)
code = compile(node, "<eval>", "eval")
assert eval(code) == 256
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`ast.literal_eval`** instead of `eval` for config snippets | Only constants—no function calls or imports |
| Call **`ast.fix_missing_locations`** before `compile` on generated trees | Tracebacks need line numbers |
| Prefer **`get_source_segment`** over re-parsing for refactors | Preserves comments and formatting outside the span |
| Compare node types with **`isinstance`**, not string tags | Survives renames and subclassing |

---

## See also

- [`tokenize`](../tokenize-tokenizer-for-python-source/index.md) — lower-level token stream
- [`dis`](../dis-disassembler-for-python-bytecode/index.md) — bytecode after `compile(tree, ...)`
