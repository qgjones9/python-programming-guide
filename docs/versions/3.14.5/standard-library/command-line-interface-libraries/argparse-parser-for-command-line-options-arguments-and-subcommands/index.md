# [argparse — Parser for command-line options, arguments and subcommands](https://docs.python.org/3/library/argparse.html)

The [`argparse`](https://docs.python.org/3/library/argparse.html) module (since 3.2) is the **recommended** standard-library way to build command-line interfaces. You declare arguments on an [`ArgumentParser`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser); `parse_args()` reads `sys.argv` (or a list you pass in) and returns a [`Namespace`](https://docs.python.org/3/library/argparse.html#argparse.Namespace) of attributes. Help text, usage lines, and basic error messages are generated automatically. Full reference remains on [docs.python.org](https://docs.python.org/3/library/argparse.html).

For legacy [`optparse`](../optparse-parser-for-command-line-options/index.md) code or cases needing finer control over option/positional interleaving, see [Choosing an argument parsing library](https://docs.python.org/3/library/optparse.html#choosing-an-argument-parsing-library).

---

## Core workflow — [ArgumentParser objects](https://docs.python.org/3/library/argparse.html#argumentparser-objects)

| Step | API | Role |
|------|-----|------|
| Create parser | `ArgumentParser(prog=..., description=...)` | Container for specs and global parser options |
| Add arguments | `add_argument(...)` | Positional, optional, flags, `nargs`, `choices`, `type` |
| Parse | `parse_args(argv=None)` | Returns `Namespace`; errors exit or raise per `exit_on_error` |
| Help | `print_help()` / `-h` | Auto-generated usage and argument list |

```python
# Goal: positional + optional flag + explicit argv for tests
import argparse

parser = argparse.ArgumentParser(prog="greet", description="Say hello")
parser.add_argument("name", help="Who to greet")
parser.add_argument("-c", "--count", type=int, default=1, help="Repeat count")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args(["Bob", "-c", "2", "-v"])
assert args.name == "Bob" and args.count == 2 and args.verbose is True
```

---

## Argument types and actions — [add_argument()](https://docs.python.org/3/library/argparse.html#the-add-argument-method)

| Pattern | `add_argument` sketch | Parsed attribute |
|---------|----------------------|------------------|
| Positional | `'filename'` | `str` (or `type` result) |
| Optional with value | `'-o', '--output'` | value after flag |
| Boolean flag | `'--verbose', action='store_true'` | `True` if present |
| Counter | `'-v', action='count', default=0'` | int verbosity level |
| Choices | `choices=['json', 'yaml']` | validated membership |
| List | `nargs='+'` or `'*'` | list (one or more / zero or more) |
| Append | `action='append'` | list built from repeated flags |

```python
# Goal: store_true, count action, and choices validation
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", action="count", default=0)
parser.add_argument("--fmt", choices=["json", "yaml"], default="json")
args = parser.parse_args(["-vv", "--fmt", "yaml"])
assert args.v == 2 and args.fmt == "yaml"

try:
    parser.parse_args(["--fmt", "xml"])
except SystemExit:
    pass  # argparse prints usage and exits on invalid choice
else:
    raise AssertionError("expected SystemExit for bad choice")
```

---

## Subcommands — [Sub-commands](https://docs.python.org/3/library/argparse.html#sub-commands)

Use `add_subparsers(dest='cmd')` when a program has distinct verbs (`git commit`, `git push`). Each subparser gets its own arguments; `args.cmd` records which subcommand ran.

```python
# Goal: nested subparsers with separate options
import argparse

parser = argparse.ArgumentParser(prog="tool")
subs = parser.add_subparsers(dest="command", required=True)
init_p = subs.add_parser("init", help="create project")
init_p.add_argument("path")
run_p = subs.add_parser("run", help="run server")
run_p.add_argument("--port", type=int, default=8000)

args = parser.parse_args(["init", "/tmp/proj"])
assert args.command == "init" and args.path == "/tmp/proj"

args = parser.parse_args(["run", "--port", "9000"])
assert args.command == "run" and args.port == 9000
```

---

## Parents, defaults, and 3.14 options

| Feature | Use when |
|---------|----------|
| `parents=[other_parser]` | Share common flags across subcommands |
| `argument_default=argparse.SUPPRESS` | Omit unset optional keys from namespace |
| `exit_on_error=False` | Catch `ArgumentError` in libraries/tests |
| `suggest_on_error=True` (3.14+) | Hint near-miss choice/subparser names |
| `fromfile_prefix_chars='@'` | Read extra args from `@file` |

```python
# Goal: exit_on_error=False for programmatic handling
import argparse

parser = argparse.ArgumentParser(exit_on_error=False)
parser.add_argument("--n", type=int)
try:
    parser.parse_args(["--n", "not-int"])
except argparse.ArgumentError as exc:
    assert "invalid int value" in str(exc)
else:
    raise AssertionError("expected ArgumentError")
```

---

## Migration and alternatives

| Library | Status |
|---------|--------|
| [`optparse`](../optparse-parser-for-command-line-options/index.md) | Deprecated; retained for existing code |
| [`getopt`](../../superseded-modules/getopt-c-style-parser-for-command-line-options/index.md) | C-style; mostly legacy |
| Third-party (`click`, `typer`, …) | When argparse’s defaults are too rigid |

See [Upgrading Optparse Code](https://docs.python.org/3/howto/argparse.html#upgrading-optparse-code) when migrating older projects.
