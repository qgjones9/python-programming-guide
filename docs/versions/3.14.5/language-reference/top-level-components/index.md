# [9. Top-level components](https://docs.python.org/3/reference/toplevel_components.html)

Chapter 9 describes **how the interpreter consumes source**: a whole program from a file or `-c`, a module body, one REPL line at a time, or a string passed to `exec()` / `eval()`. It does not prescribe your shell or IDE—only the grammars that apply in each situation. Normative wording is on [docs.python.org](https://docs.python.org/3/reference/toplevel_components.html); this page orients you and links child notes.

Related chapters: [Execution model](../execution-model/index.md) (`__main__`, namespaces), [Simple](../simple-statements/index.md) and [Compound](../compound-statements/index.md) statements (what gets parsed inside `file_input`), and [The import system](../the-import-system/index.md) (module loading uses the same file grammar).

---

## Input modes at a glance

| Mode | Grammar (reference) | Typical source |
|------|---------------------|----------------|
| Complete program / module / `exec()` | `file_input` | `.py` file, `python -m`, `exec(compile(...))` |
| Interactive REPL | `interactive_input` | Typed statements in `python` on a TTY |
| `eval()` | `eval_input` | `eval("expression")`, calculator-style strings |

A **complete program** runs in a minimally initialized environment: built-in and standard modules exist but are not initialized except `sys`, `builtins`, and `__main__` (the global namespace for top-level code). The same startup picture applies to interactive mode, but the REPL reads **one** statement (or compound statement) per prompt instead of a whole file until `ENDMARKER`.

---

## Choosing which section to read

| Question | Section |
|----------|---------|
| What counts as “running a script” vs the REPL? | [9.1 Complete Python programs](complete-python-programs/index.md) |
| Grammar for `.py` files and `exec()` strings? | [9.2 File input](file-input/index.md) |
| Why does my `for` loop need an extra blank line in the shell? | [9.3 Interactive input](interactive-input/index.md) |
| What may I pass to `eval()`? | [9.4 Expression input](expression-input/index.md) |

```python
# Goal: top-level bindings live in __main__ (complete program / script semantics)
import __main__

__main__.marker = "run"
assert __main__.marker == "run"
```

```python
# Goal: file_input-shaped code via compile + exec (same grammar as a .py module body)
src = "total = sum(range(4))\n"
ns: dict[str, object] = {}
exec(compile(src, "<module>", "exec"), ns, ns)
assert ns["total"] == 6
```

```python
# Goal: eval_input — expression_list only, not statements
assert eval("2 ** 10") == 1024
assert eval("(1, 2, 3)") == (1, 2, 3)
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [9.1. Complete Python programs](complete-python-programs/index.md) | Minimal startup environment, `__main__`, and three ways to hand the interpreter a full program (`-c`, file argv, stdin). |
| [9.2. File input](file-input/index.md) | `file_input` grammar: statements until `ENDMARKER`; used for programs, modules, and `exec()`. |
| [9.3. Interactive input](interactive-input/index.md) | REPL grammar; compound statements require a trailing blank line so the parser sees end of input. |
| [9.4. Expression input](expression-input/index.md) | `eval_input` for `eval()`: `expression_list` plus optional newlines, then `ENDMARKER`. |
