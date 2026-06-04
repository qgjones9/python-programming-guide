# [The Python Language Reference](https://docs.python.org/3/reference/index.html#reference-index)

The [language reference](https://docs.python.org/3/reference/index.html) is the **normative, terse** description of Python syntax and core semantics. It is meant to be exact and complete for language lawyers and implementers; it is not a tutorial. Builtin types, functions, and standard modules are specified in [The Python Standard Library](../standard-library/index.md). For a guided introduction, use [The Tutorial](../tutorial/index.md). C/C++ extension authors should also read [Python/C API](../python-c-api-reference-manual/index.md) and [Extending and Embedding](../extending-and-embedding-python-interpreter/index.md).

This repo mirrors the official outline under `docs/versions/3.14.5/language-reference/`. Each chapter `index.md` links to the canonical `reference/*.html` page; teaching bullets and small `exec`-validated examples live here—full prose and the complete grammar remain on docs.python.org.

---

## Choosing the right manual

| You need… | Start here |
|-----------|------------|
| “How do I write Python?” step by step | [The Tutorial](../tutorial/index.md) |
| “What does this statement/expression *mean*?” | Language reference (this tree) |
| “What does `json.loads` / `pathlib` do?” | [Standard Library](../standard-library/index.md) |
| Embedding, `PyObject*`, GIL | [C API](../python-c-api-reference-manual/index.md) + [Extending](../extending-and-embedding-python-interpreter/index.md) |
| Full EBNF grammar rules | [Full Grammar specification](full-grammar-specification/index.md) |

| Reading order (first pass) | Why |
|----------------------------|-----|
| [Introduction](introduction/index.md) → [Lexical analysis](lexical-analysis/index.md) | Tokens, indentation, literals before syntax |
| [Data model](data-model/index.md) → [Execution model](execution-model/index.md) | Objects, binding, exceptions, frames |
| [The import system](the-import-system/index.md) | How modules load before you rely on `import` |
| [Expressions](expressions/index.md) → [Simple](simple-statements/index.md) / [Compound](compound-statements/index.md) statements | Syntax and semantics of code you write daily |
| [Top-level components](top-level-components/index.md) | How scripts, modules, `exec`, and `eval` are parsed |
| [Full Grammar specification](full-grammar-specification/index.md) | When you need the formal production rules |

---

## Sections in this repo

| Chapter | Summary |
|---------|---------|
| [1. Introduction](introduction/index.md) | Scope of the reference, alternate implementations, and BNF notation used in later chapters. |
| [2. Lexical analysis](lexical-analysis/index.md) | Source structure: lines, indentation, identifiers, literals, operators, and encoding. |
| [3. Data model](data-model/index.md) | Objects, values, types, the standard hierarchy, special methods, and coroutines. |
| [4. Execution model](execution-model/index.md) | Program structure, namespaces, binding rules, exceptions, and runtime components. |
| [5. The import system](the-import-system/index.md) | `importlib`, packages, finders, loaders, and customizing import. |
| [6. Expressions](expressions/index.md) | Atoms, operators, comprehensions, lambdas, and expression grammar. |
| [7. Simple statements](simple-statements/index.md) | Assignment, `assert`, `return`, `import`, `raise`, and other one-line statements. |
| [8. Compound statements](compound-statements/index.md) | `if`, loops, `try`, `with`, functions, classes, and pattern matching. |
| [9. Top-level components](top-level-components/index.md) | Complete programs, file/module/`exec` input, REPL input, and `eval` input. |
| [10. Full Grammar specification](full-grammar-specification/index.md) | Entire Python grammar in one formal specification. |
