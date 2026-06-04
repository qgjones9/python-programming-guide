# [PEG](https://docs.python.org/3/reference/introduction.html#notation)

Local notes on **PEG** (Parsing Expression Grammar) ideas used in Python's grammar notation, within [*Notation*](../index.md). Python's reference mixes classic EBNF-style rules with PEG **ordered choice**. CPython has used a PEG-based parser since 3.9 ([PEP 617](https://peps.python.org/pep-0617/)).

PEG grammars describe how a parser **attempts** to match input: alternatives are tried **in written order**, and the first successful match wins. That differs from many context-free grammars where a parser generator must **predict** which alternative applies from one token of lookahead alone.

## Ordered choice

In traditional PEG notation, ordered choice is often written with a slash:

```ebnf
rule: A / B / C
```

Python's reference uses a vertical bar with the same **ordered** semantics ([PEP 617](https://peps.python.org/pep-0617/)):

```ebnf
rule: A | B | C
```

| Behavior | Meaning |
|----------|---------|
| Try `A` first | If `A` matches, stop; do not consider `B` or `C`. |
| `A` fails | Backtrack and try `B`, then `C` if needed. |
| Not commutative | `A \| B` and `B \| A` can parse different inputs. |

This removes a class of ambiguities that troubled the old LL(1) grammar: if two alternatives could start with the same token, an LL(1) parser could not decide between them without rewriting the rules.

## PEG vs classic EBNF choice

| Aspect | Classic EBNF (LL-style) | PEG ordered choice |
|--------|-------------------------|---------------------|
| Alternative selection | Often requires disjoint FIRST sets | First successful match in source order |
| Ambiguity | Grammar may be ambiguous | Each input has at most one parse tree |
| Left recursion | Handled with parser tables or transforms | Natural in PEG with direct encoding |
| Notation in Python docs | Same `\|` symbol | Same `\|` symbol, PEG semantics |

For EBNF building blocks (sequences, `{ }`, `[ ]`), see [EBNF](../ebnf/index.md). For the full symbol reference used in Python rules, see [Python's grammar notation](../index.md).

## CPython's PEG parser (PEP 617)

Before Python 3.9, CPython used an LL(1) parser with workarounds for constructs LL(1) cannot express naturally. [PEP 617](https://peps.python.org/pep-0617/) replaced it with a PEG parser generated from the grammar in the reference. Benefits include:

| Benefit | Detail |
|---------|--------|
| Clearer grammar | Fewer "hacks" to satisfy LL(1) restrictions. |
| Unambiguous parses | One valid parse tree per accepted program. |
| Maintainability | Grammar, parser, and AST pipeline align more closely. |

The authoritative grammar lives in [Full Grammar specification](../../../full-grammar-specification/index.md). Lexical rules in [Lexical analysis](../../../lexical-analysis/index.md) still use the same notation; remember that lexical rules operate on **characters**, while syntactic rules operate on **tokens**.

## Lookaheads in PEG

PEG also uses predicates that inspect input without consuming it (documented in [Notation](../index.md)):

| Notation | Name | Effect |
|----------|------|--------|
| `&e` | Positive lookahead | Succeeds only if `e` would match here; input position unchanged. |
| `!e` | Negative lookahead | Succeeds only if `e` would **not** match here. |

Lookaheads disambiguate cases where a simple sequence or alternative would be unclear.

## Best practices

| Practice | Why |
|----------|-----|
| Remember `\|` is **ordered** when reading Python grammar rules. | Reordering alternatives can change the language. |
| Use [EBNF](../ebnf/index.md) intuition for structure, PEG for choice. | Sequences and repetition work like familiar EBNF; choice does not. |
| Validate edge-case syntax with `ast.parse` on your target version. | The parser enforces the grammar; English summaries can lag. |
| Compare against [Full Grammar specification](../../../full-grammar-specification/index.md) for formal disputes. | PEP 617 notes that the grammar chapter is canonical for syntax. |

```python
import ast

# CPython's PEG parser accepts well-formed statements.
tree = ast.parse("if True:\n    pass\n")
assert isinstance(tree.body[0], ast.If)

# Malformed syntax raises SyntaxError—the grammar rejects ordered-choice failures too.
try:
    ast.parse("if True pass")  # missing colon
except SyntaxError:
    pass
else:
    raise AssertionError("expected SyntaxError for invalid if-statement")
```

Parent: [Notation](../index.md)
