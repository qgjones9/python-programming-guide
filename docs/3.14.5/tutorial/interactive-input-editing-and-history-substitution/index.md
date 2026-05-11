# [Interactive Input Editing and History Substitution](https://docs.python.org/3/tutorial/interactive.html)

Condensed notes for [chapter 14](https://docs.python.org/3/tutorial/interactive.html): GNU **Readline** integration (history, completion) and alternatives like **IPython** / **Jupyter**.

```python
import sys

# Readline is optional — some builds omit it; guard features behind `import readline` in apps.
try:
    import readline  # noqa: F401 — importing side effects hook line editing when present
except ImportError:
    readline = None

assert readline is None or hasattr(readline, "parse_and_bind")
```

## Sections in this repo

- [Tab Completion and History Editing](tab-completion-and-history-editing/index.md)
- [Alternatives to the Interactive Interpreter](alternatives-to-the-interactive-interpreter/index.md)

Next: [Floating-Point Arithmetic: Issues and Limitations](../floating-point-arithmetic-issues-and-limitations/index.md)
