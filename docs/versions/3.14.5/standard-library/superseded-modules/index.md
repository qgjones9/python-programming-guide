# [Superseded Modules](https://docs.python.org/3/library/superseded.html)

The **Superseded Modules** chapter lists standard-library modules that remain for **backward compatibility** but are no longer the recommended tool for most tasks. Full API reference stays on [docs.python.org](https://docs.python.org/3/library/superseded.html); this hub explains why they linger, how to choose a modern replacement, and where local notes live in this repo.

---

## Why modules are superseded

| Reason | What it means | What to do in new code |
|--------|---------------|------------------------|
| **Narrow scope** | Covers one legacy API shape (for example mimicking C `getopt()`) | Use a broader stdlib module (`argparse`) or a maintained third-party library |
| **Soft deprecation** | Still importable; docs discourage new use | Plan migration; avoid new dependencies on the old API |
| **Awaiting removal** | Marked for deletion in a future release | Treat as removed; migrate immediately |

After [PEP 594](https://peps.python.org/pep-0594/) removed many obsolete modules, CPython currently lists **no** modules in the “soft deprecated, awaiting removal” bucket on this page—only compatibility-oriented superseded APIs such as [`getopt`](getopt-c-style-parser-for-command-line-options/index.md).

---

## Migration mindset

| Situation | Recommended path |
|-----------|------------------|
| Greenfield CLI | [`argparse`](../command-line-interface-libraries/argparse-parser-for-command-line-options-arguments-and-subcommands/index.md) (declarative, subcommands, help generation) |
| Legacy script already using C-style short options | Keep [`getopt`](getopt-c-style-parser-for-command-line-options/index.md) only while porting; map option letters to `argparse` actions |
| Module listed under [Removed Modules](../removed-modules/index.md) | Do **not** import from stdlib—use the replacement in the removed-modules table or a vetted PyPI package |

---

## Module index

| Module | Role (legacy) | Modern replacement |
|--------|---------------|-------------------|
| [`getopt`](getopt-c-style-parser-for-command-line-options/index.md) | Parse `sys.argv` like Unix `getopt(3)` | [`argparse`](../command-line-interface-libraries/argparse-parser-for-command-line-options-arguments-and-subcommands/index.md); [`optparse`](../command-line-interface-libraries/optparse-parser-for-command-line-options/index.md) is also legacy |

---

## Quick comparison — CLI parsing

```python
# Goal: same short options with getopt (legacy C-style API)
import getopt
import sys

argv = ["script.py", "-v", "-o", "out.txt", "input.txt"]
opts, args = getopt.getopt(argv[1:], "vo:", ["verbose"])
opt_dict = dict(opts)
assert opt_dict["-v"] == ""
assert opt_dict["-o"] == "out.txt"
assert args == ["input.txt"]
```

```python
# Goal: equivalent flags with argparse (preferred for new scripts)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-o", metavar="FILE")
parser.add_argument("input", nargs=1)
ns = parser.parse_args(["-v", "-o", "out.txt", "input.txt"])
assert ns.verbose is True
assert ns.o == "out.txt"
assert ns.input == ["input.txt"]
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [getopt — C-style parser for command line options](getopt-c-style-parser-for-command-line-options/index.md) | `getopt()`, `gnu_getopt()`, `GetoptError`, migration to `argparse` |
