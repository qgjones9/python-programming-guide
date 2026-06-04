# [Introduction](https://docs.python.org/3/reference/introduction.html)

Local notes for [**Introduction**](https://docs.python.org/3/reference/introduction.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This chapter orients you to what the reference is—and is not—before you read the formal grammar and semantics chapters. Normative wording lives on docs.python.org.

This reference manual describes the Python programming language. It is **not** a tutorial. Most prose uses English rather than formal logic, except for syntax and lexical analysis, where the grammar notation is precise. Short **implementation notes** appear where CPython behavior matters for understanding the language definition.

Every Python implementation ships built-in and standard modules documented in [The Python Standard Library](../../standard-library/index.md). A few built-ins are mentioned here when they interact with the language definition itself.

## What this chapter covers

| Section | Focus |
|---------|-------|
| [Alternate Implementations](alternate-implementations/index.md) | CPython and other runtimes (Jython, PyPy, .NET ports) and how they relate to this manual. |
| [Notation](notation/index.md) | The EBNF/PEG grammar notation used in lexical and syntactic rules throughout the reference. |

## Reference vs tutorial

| Resource | Best for |
|----------|----------|
| [The Tutorial](../../tutorial/index.md) | Learning Python step by step with examples. |
| [This Language Reference](../index.md) | Precise rules about syntax, semantics, imports, and execution. |
| [The Standard Library](../../standard-library/index.md) | Built-in modules and their APIs. |

When you need *why* to use a feature, start with the tutorial. When you need *whether* a construct is legal or what it means, use this reference.

## Best practices

| Practice | Why |
|----------|-----|
| Treat CPython as the default semantics unless you target another runtime. | Most examples and implementation notes assume CPython. |
| Follow canonical section anchors on docs.python.org when citing rules. | Minor releases can add footnotes or clarify edge cases. |
| Read [Notation](notation/index.md) before [Lexical analysis](../lexical-analysis/index.md). | Later chapters assume you can read grammar rules. |
| Check implementation-specific docs when not on CPython. | Alternate runtimes may differ from this manual. |
| Distinguish language rules from library behavior. | The reference defines the core language; modules are documented separately. |

```python
import sys

# The reference describes language semantics; the active runtime reports its implementation.
assert sys.implementation.name is not None
assert sys.version_info.major >= 3
```

## Sections in this repo

| Section | Path |
|---------|------|
| [Alternate Implementations](alternate-implementations/index.md) | `alternate-implementations/index.md` |
| [Notation](notation/index.md) | `notation/index.md` |
