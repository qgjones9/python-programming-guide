# [Appendix](https://docs.python.org/3/tutorial/appendix.html)

Condensed notes for [Appendix — Interactive Input Editing](https://docs.python.org/3/tutorial/appendix.html): startup files, script shebang lines, error handling in interactive mode, and customization hooks.

```python
import sys

# Interactive vs script mode is reflected in `sys.flags` (inspect interactively for details).
assert hasattr(sys.flags, "interactive")
```

## Sections in this repo

- [Interactive Mode](interactive-mode/index.md)

Related: [Interactive Input Editing and History Substitution](../interactive-input-editing-and-history-substitution/index.md) (chapter 14).
