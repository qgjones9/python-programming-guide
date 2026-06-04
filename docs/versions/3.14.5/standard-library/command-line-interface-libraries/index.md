# [Command-line interface libraries](https://docs.python.org/3/library/cmdlinelibs.html)

Python’s standard library groups **argument parsing**, **interactive shells**, **password prompts**, **multi-file line iteration**, and **terminal UI (TUI)** helpers under **Command-line interface libraries**. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/cmdlinelibs.html); this hub orients you to each module, when to reach for it, and how the pieces fit together.

Related material outside this section: the interpreter’s own [command-line interface](https://docs.python.org/3/using/cmdline.html), [modules with a built-in CLI](../modules-command-line-interface-cli/index.md) (`python -m …`), and superseded [`getopt`](../superseded-modules/getopt-c-style-parser-for-command-line-options/index.md) for C-style option parsing.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`argparse`](argparse-parser-for-command-line-options-arguments-and-subcommands/index.md) | Declarative CLI: positional args, options, subcommands, auto-generated help |
| [`optparse`](optparse-parser-for-command-line-options/index.md) | Legacy declarative option parser; finer control over option/arg interleaving |
| [`getpass`](getpass-portable-password-input/index.md) | Hidden (or masked) password prompts and login-name lookup |
| [`fileinput`](fileinput-iterate-over-lines-from-multiple-input-streams/index.md) | Iterate lines across `sys.argv` files, `-`, gzip/bz2 hooks, in-place filter |
| [`curses`](curses-terminal-handling-for-character-cell-displays/index.md) | Portable TUI: windows, colors, input, screen control |
| [`curses.textpad`](cursestextpad-text-input-widget-for-curses-programs/index.md) | Emacs-like editable text widget inside a curses window |
| [`curses.ascii`](cursesascii-utilities-for-ascii-characters/index.md) | ASCII class tests and control-character helpers (no TTY required) |
| [`curses.panel`](cursespanel-a-panel-stack-extension-for-curses/index.md) | Z-ordered panel stack over curses windows |
| [`cmd`](cmd-support-for-line-oriented-command-interpreters/index.md) | Line-oriented REPL/shell framework (`do_*` dispatch, tab completion) |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| New CLI with subcommands and `--help` | [`argparse`](argparse-parser-for-command-line-options-arguments-and-subcommands/index.md) |
| Legacy code or strict option/positional interleaving | [`optparse`](optparse-parser-for-command-line-options/index.md) |
| Prompt for secrets without echo | [`getpass`](getpass-portable-password-input/index.md) |
| `grep`-style tool over many files / stdin | [`fileinput`](fileinput-iterate-over-lines-from-multiple-input-streams/index.md) |
| Full-screen terminal app (menus, forms) | [`curses`](curses-terminal-handling-for-character-cell-displays/index.md) + submodules |
| Admin shell inside your program | [`cmd`](cmd-support-for-line-oriented-command-interpreters/index.md) |
| Classify or display ASCII control chars | [`curses.ascii`](cursesascii-utilities-for-ascii-characters/index.md) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Prefer **`argparse`** for new projects | Rich defaults (help, subparsers, `nargs`, choices) with less boilerplate |
| Use **`parse_args(['--', ...])`** in tests | Avoid mutating `sys.argv`; pass explicit token lists |
| Guard **`curses`** imports on mobile/WASI | Module is unavailable on Android, iOS, and WebAssembly |
| Set **`fileinput.input(encoding='utf-8')`** explicitly | Text mode defaults depend on locale; be explicit for portable tools |
| Subclass **`cmd.Cmd`**, don’t instantiate it bare | Framework is meant for `do_*` / `help_*` hooks on your shell class |
| Never log **`getpass`** output | Passwords must not appear in logs, history, or echoed streams |

```python
# Goal: parse argv in tests without touching sys.argv
import argparse

parser = argparse.ArgumentParser(prog="demo")
parser.add_argument("name")
args = parser.parse_args(["alice"])
assert args.name == "alice"
```

```python
# Goal: dispatch one line in a cmd-style shell without a TTY loop
import cmd
import io

class MiniShell(cmd.Cmd):
    prompt = "> "
    def do_echo(self, arg):
        self.last = arg

shell = MiniShell(stdin=io.StringIO(), stdout=io.StringIO())
shell.use_rawinput = False
shell.onecmd("echo hello")
assert shell.last == "hello"
```

---

## Sections in this repo

| Module | Notes |
|--------|-------|
| [argparse — Parser for command-line options, arguments and subcommands](argparse-parser-for-command-line-options-arguments-and-subcommands/index.md) | `ArgumentParser`, subparsers, actions, namespaces |
| [optparse — Parser for command line options](optparse-parser-for-command-line-options/index.md) | `OptionParser`, `(options, args)` tuple, migration notes |
| [getpass — Portable password input](getpass-portable-password-input/index.md) | `getpass()`, `getuser()`, `echo_char` (3.14+) |
| [fileinput — Iterate over lines from multiple input streams](fileinput-iterate-over-lines-from-multiple-input-streams/index.md) | `input()`, inplace mode, compressed hooks |
| [curses — Terminal handling for character-cell displays](curses-terminal-handling-for-character-cell-displays/index.md) | Windows, colors, `wrapper()`, input |
| [curses.textpad — Text input widget for curses programs](cursestextpad-text-input-widget-for-curses-programs/index.md) | `Textbox`, Emacs-like editing |
| [curses.ascii — Utilities for ASCII characters](cursesascii-utilities-for-ascii-characters/index.md) | `isalnum`, `ctrl`, `unctrl`, control names |
| [curses.panel — A panel stack extension for curses](cursespanel-a-panel-stack-extension-for-curses/index.md) | `panel()`, depth ordering, `update_panels` |
| [cmd — Support for line-oriented command interpreters](cmd-support-for-line-oriented-command-interpreters/index.md) | `Cmd`, `cmdloop`, completion hooks |
