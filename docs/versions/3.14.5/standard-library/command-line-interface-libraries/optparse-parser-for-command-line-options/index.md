# [optparse — Parser for command line options](https://docs.python.org/3/library/optparse.html)

The [`optparse`](https://docs.python.org/3/library/optparse.html) module provides a **declarative** option parser that predates [`argparse`](argparse-parser-for-command-line-options-arguments-and-subcommands/index.md). `OptionParser.parse_args()` returns **`(options, args)`** — an [`Values`](https://docs.python.org/3/library/optparse.html#optparse.Values) object and a **separate list of positional arguments**. The module is **deprecated** since Python 3.2; new code should use argparse unless you need optparse-specific parsing behavior. Full API remains on [docs.python.org](https://docs.python.org/3/library/optparse.html).

---

## When to keep optparse — [Choosing an argument parsing library](https://docs.python.org/3/library/optparse.html#choosing-an-argument-parsing-library)

| Scenario | Why optparse |
|----------|--------------|
| Existing large codebase | Avoid subtle migration behavior changes |
| Strict interleaving control | Options and positionals processed in separate phases |
| Values starting with `-` for `-o` | e.g. `-o -v` can mean `output="-v"` (argparse rejects) |
| Incremental / low-level parsing | Foundation for third-party libraries (e.g. early `click`) |

---

## Basic usage — [Introduction](https://docs.python.org/3/library/optparse.html#introduction)

| Component | Role |
|-----------|------|
| `OptionParser()` | Holds option definitions |
| `add_option('-f', '--file', dest='filename', ...)` | Register short/long options |
| `parse_args()` | Returns `(options, positional_args)` |
| `options.filename` | Attribute from `dest` (defaults to long opt name) |

```python
# Goal: options tuple separate from positional args
import optparse

parser = optparse.OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
parser.add_option("-o", "--output", dest="output")
opts, args = parser.parse_args(["-v", "-o", "out.txt", "input.dat", "extra"])
assert opts.verbose is True
assert opts.output == "out.txt"
assert args == ["input.dat", "extra"]
```

---

## Common option actions

| `action` | Effect |
|----------|--------|
| `'store'` (default) | Save the next argv token |
| `'store_true'` / `'store_false'` | Set boolean without consuming a value |
| `'append'` | Build a list from repeated occurrences |
| `'count'` | Increment an integer (`-vvv` → 3) |
| `'callback'` | Custom handler (advanced) |

```python
# Goal: count and append actions
import optparse

parser = optparse.OptionParser()
parser.add_option("-v", action="count", dest="verbosity", default=0)
parser.add_option("-D", action="append", dest="defines", default=[])
opts, args = parser.parse_args(["-vv", "-D", "DEBUG", "-D", "FAST", "file"])
assert opts.verbosity == 2
assert opts.defines == ["DEBUG", "FAST"]
assert args == ["file"]
```

---

## Behavioral differences from argparse

| Input | optparse | argparse |
|-------|----------|----------|
| `-o -v` ( `-o` takes a value) | `output="-v"`, verbose unset | Usage error ( `-v` not a value for `-o`) |
| `-o=foo` | `output="=foo"` (literal) | `output="foo"` (`=` is special) |
| Positional args | Returned as second tuple element | Declared with `add_argument('name')` on same parser |

```python
# Goal: optparse accepts -v as the argument to -o
import optparse

parser = optparse.OptionParser()
parser.add_option("-o", "--output", dest="output")
parser.add_option("-v", dest="verbose", action="store_true")
opts, args = parser.parse_args(["-o", "-v"])
assert opts.output == "-v" and not opts.verbose and args == []
```

---

## Types, defaults, and help

| Parameter | Notes |
|-----------|-------|
| `type='int'` / `'float'` / `'string'` | Coerce option values |
| `default=` | Initial attribute on `Values` |
| `help=` | Shown in `--help` output |
| `metavar='FILE'` | Placeholder name in usage |

```python
# Goal: typed option with default
import optparse

parser = optparse.OptionParser()
parser.add_option("-n", type="int", dest="count", default=10)
opts, _ = parser.parse_args(["-n", "3"])
assert opts.count == 3
opts2, _ = parser.parse_args([])
assert opts2.count == 10
```

---

## Migration

See [Upgrading Optparse Code](https://docs.python.org/3/howto/argparse.html#upgrading-optparse-code) for a side-by-side translation to [`argparse`](argparse-parser-for-command-line-options-arguments-and-subcommands/index.md). Key change: positional arguments become first-class `add_argument()` entries, and `parse_args()` returns a single namespace instead of a tuple.
