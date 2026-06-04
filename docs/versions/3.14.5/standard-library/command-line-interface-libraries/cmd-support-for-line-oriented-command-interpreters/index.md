# [cmd — Support for line-oriented command interpreters](https://docs.python.org/3/library/cmd.html)

The [`cmd`](https://docs.python.org/3/library/cmd.html) module provides a **line-oriented command interpreter** framework. Subclass [`Cmd`](https://docs.python.org/3/library/cmd.html#cmd.Cmd), implement `do_commandname()` methods, and run [`cmdloop()`](https://docs.python.org/3/library/cmd.html#cmd.Cmd.cmdloop) for an interactive shell with help, history (via [`readline`](../text-processing-services/readline-gnu-readline-interface/index.md)), and tab completion. Ideal for admin tools, test harnesses, and prototypes. Full API remains on [docs.python.org](https://docs.python.org/3/library/cmd.html).

---

## Dispatch model — [Cmd Objects](https://docs.python.org/3/library/cmd.html#cmd-objects)

| User input | Handler |
|------------|---------|
| `foo arg1 arg2` | `do_foo(self, 'arg1 arg2')` |
| `?` or `help` | `do_help()` — lists commands |
| `help foo` | `help_foo()` or docstring of `do_foo` |
| `!shellcmd` | `do_shell()` if defined |
| Empty line | `emptyline()` — default repeats last command |
| Unknown verb | `default(line)` |

```python
# Goal: onecmd dispatches to do_* without running cmdloop
import cmd
import io

class Calc(cmd.Cmd):
    prompt = "(calc) "
    def do_add(self, arg):
        self.result = sum(int(x) for x in arg.split())
    def do_quit(self, arg):
        return True  # stop loop when using cmdloop

shell = Calc(stdin=io.StringIO(), stdout=io.StringIO())
shell.use_rawinput = False
assert shell.onecmd("add 1 2 3") is None
assert shell.result == 6
assert shell.onecmd("quit") is True
```

---

## Hooks and control flow

| Method | When it runs |
|--------|--------------|
| `preloop()` | Once before `cmdloop()` |
| `precmd(line)` | In **`cmdloop()`** only: after prompt, before dispatch; may rewrite `line` |
| `postcmd(stop, line)` | In **`cmdloop()`** only: after command; return value becomes new stop flag |
| `postloop()` | Once when loop exits |

```python
# Goal: precmd normalizes input (cmdloop calls precmd before onecmd)
import cmd
import io

class Shell(cmd.Cmd):
    def do_echo(self, arg):
        self.echoed = arg
    def precmd(self, line):
        return line.strip().lower()

s = Shell(stdin=io.StringIO(), stdout=io.StringIO())
s.use_rawinput = False
line = s.precmd("  ECHO   Hello  ")
s.onecmd(line)
assert s.echoed == "hello"
```

---

## Completion

When `readline` is available and `completekey` is not `None` (default `'tab'`), command names complete automatically. Define `complete_foo(self, text, line, begidx, endidx)` to complete arguments for `foo`.

```python
# Goal: complete_* returns prefixes for tab completion
import cmd

class Shell(cmd.Cmd):
    fruits = ["apple", "apricot", "banana"]
    def do_pick(self, arg):
        pass
    def complete_pick(self, text, line, begidx, endidx):
        return [f for f in self.fruits if f.startswith(text)]

s = Shell()
matches = s.complete_pick("ap", "pick ap", 5, 7)
assert set(matches) == {"apple", "apricot"}
```

---

## Instance attributes

| Attribute | Default | Role |
|-----------|---------|------|
| `prompt` | `'(Cmd) '` | Shown each iteration |
| `intro` | `None` | Banner before first prompt |
| `identchars` | letters + `_` + digits | Valid command name chars |
| `cmdqueue` | `[]` | Preloaded lines processed before stdin |
| `use_rawinput` | `True` | Use `input()` vs raw readline |
| `lastcmd` | `''` | Previous non-empty command |

```python
# Goal: cmdqueue replays scripted commands
import cmd
import io

class Shell(cmd.Cmd):
    def do_step(self, arg):
        self.steps = getattr(self, "steps", []) + [arg]

s = Shell(stdin=io.StringIO(), stdout=io.StringIO())
s.use_rawinput = False
s.cmdqueue = ["step one", "step two"]
s.onecmd("")  # triggers processing from queue on next cmdloop iteration
# Process queue manually via onecmd for deterministic test:
for line in ["step one", "step two"]:
    s.onecmd(line)
assert s.steps == ["one", "two"]
```

---

## Help and formatting

`do_help()` with no args lists documented commands (`help_*` or docstrings). `columnize(list, displaywidth=80)` prints compact columns.

```python
# Goal: help uses do_* docstring when help_* missing
import cmd
import io

class Shell(cmd.Cmd):
    def do_ping(self, arg):
        """Respond to ping."""
        pass

s = Shell(stdin=io.StringIO(), stdout=io.StringIO())
out = io.StringIO()
s.stdout = out
s.onecmd("help ping")
assert "Respond to ping" in out.getvalue()
```

---

## Related modules

| Module | Use with cmd |
|--------|--------------|
| [`readline`](../text-processing-services/readline-gnu-readline-interface/index.md) | History and completion backend |
| [`argparse`](argparse-parser-for-command-line-options-arguments-and-subcommands/index.md) | Non-interactive CLI alongside an optional cmd shell |
| [`shlex`](https://docs.python.org/3/library/shlex.html) | Parse quoted arguments inside `do_*` handlers |
