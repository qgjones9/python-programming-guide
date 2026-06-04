# [getopt — C-style parser for command line options](https://docs.python.org/3/library/getopt.html)

[`getopt`](https://docs.python.org/3/library/getopt.html) parses **`sys.argv`-style** option lists using the same conventions as Unix **`getopt(3)`** (short options, optional `:` / `::` arguments, `--` terminator, and long options via `getopt.long_options`). The module is **feature complete** and retained for scripts that must stay byte-compatible with C tooling. For new projects, prefer [`argparse`](../../command-line-interface-libraries/argparse-parser-for-command-line-options-arguments-and-subcommands/index.md).

---

## API surface

| Name | Purpose |
|------|---------|
| `getopt(args, shortopts, longopts=[])` | POSIX-style scan; stops at first non-option unless GNU rules apply |
| `gnu_getopt(args, shortopts, longopts=[])` | GNU-style scan; options and operands may be interleaved |
| `GetoptError` | Raised on unknown options or missing arguments (`msg`, `opt`) |
| `error` | Alias for `GetoptError` (backward compatibility) |

**`shortopts`:** option letters; a letter followed by **`:`** requires an argument; **`::`** means an optional argument (GNU extension).

**`longopts`:** list of strings `"name"` or `"name="` (required arg) or `"name::"` (optional arg).

---

## When to keep vs replace

| Keep `getopt` | Migrate to `argparse` |
|---------------|----------------------|
| Porting a C `getopt` driver line-for-line | Need `--help`, subcommands, or type checking |
| Tiny script with only `-h` and one `-oFILE` | Want `nargs`, choices, or mutually exclusive groups |
| External spec mandates `getopt` option strings | Teaching or maintaining long-term CLI UX |

[`optparse`](../../command-line-interface-libraries/optparse-parser-for-command-line-options/index.md) is also superseded by `argparse` but offers a more declarative style than raw `getopt`.

---

## POSIX vs GNU scanning

```python
# Goal: POSIX mode stops at first non-option argument
import getopt

opts, rest = getopt.getopt(["-a", "file", "-b"], "ab")
assert [o[0] for o in opts] == ["-a"]
assert rest == ["file", "-b"]  # -b is not parsed as an option
```

```python
# Goal: GNU mode can parse options after operands
import getopt

opts, rest = getopt.gnu_getopt(["file", "-b"], "ab", [])
assert ("-b", "") in opts
assert rest == ["file"]
```

---

## Long options and errors

```python
import getopt

opts, args = getopt.getopt(
    ["--output=out.txt", "pos"],
    "o:",
    ["output="],
)
assert dict(opts)["--output"] == "out.txt"
assert args == ["pos"]

try:
    getopt.getopt(["-z"], "a")
except getopt.GetoptError as exc:
    assert "not recognized" in str(exc).lower() or exc.opt == "-z"
```

---

## Migration — same flags with `argparse`

```python
# Goal: map legacy "-oFILE" / "--output=FILE" to argparse
import argparse

parser = argparse.ArgumentParser(prog="tool")
parser.add_argument("-o", "--output", required=True)
parser.add_argument("paths", nargs="+")
ns = parser.parse_args(["-o", "out.txt", "a", "b"])
assert ns.output == "out.txt"
assert ns.paths == ["a", "b"]
```

```python
# Goal: optional GNU-style argument with argparse (long option)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--color", nargs="?", const="always", default=None)
assert parser.parse_args(["--color"]).color == "always"
assert parser.parse_args(["--color", "never"]).color == "never"
assert parser.parse_args([]).color is None
```

---

## See also

- [Superseded Modules hub](../index.md)
- [`argparse` — Parser for command-line options, arguments and subcommands](../../command-line-interface-libraries/argparse-parser-for-command-line-options-arguments-and-subcommands/index.md)
- [Removed Modules](../../removed-modules/index.md) — modules no longer importable from the stdlib
