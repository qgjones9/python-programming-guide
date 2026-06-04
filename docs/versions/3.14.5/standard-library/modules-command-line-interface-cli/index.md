# [Modules command-line interface (CLI)](https://docs.python.org/3/library/cmdline.html)

Several standard-library modules expose a **command-line interface** when invoked with **`python -m module`**. This page lists those entry points and how they relate to the interpreter’s own flags. Full details remain on [docs.python.org](https://docs.python.org/3/library/cmdline.html); see also [Using Python — Command line](https://docs.python.org/3/using/cmdline.html) for `python` itself.

---

## Modules with a documented CLI

| Module | How to run | Role |
|--------|------------|------|
| **`cProfile`** | `python -m cProfile script.py` | Profile a script (see [`profile` / `cProfile`](../debugging-and-profiling/index.md)) |
| **`encodings.rot_13`** | `python -m encodings.rot_13` | ROT-13 filter on stdin/stdout (codec demo) |
| **`this`** | `python -m this` | Prints *The Zen of Python* |

The upstream index also notes **`profile`** as the CLI surface for **`cProfile`** (same profiling workflow; `cProfile` is the recommended implementation).

---

## Typical patterns

| Pattern | Example | Notes |
|---------|---------|-------|
| Run module as filter | `python -m encodings.rot_13 < file.txt` | Reads stdin, writes stdout |
| Run module as tool | `python -m cProfile -s cumtime myapp.py` | Forwards args to the module’s `__main__` |
| Discover help | `python -m cProfile --help` | Many `-m` modules accept `-h` / `--help` |

```python
# Goal: ROT-13 via the encodings.rot_13 codec (same transform as python -m encodings.rot_13)
import codecs

plain = "The Zen of Python"
encoded = codecs.encode(plain, "rot_13")
assert encoded == "Gur Mra bs Clguba"
assert codecs.decode(encoded, "rot_13") == plain
```

```python
# Goal: this.s stores ROT-13; decode to read the Zen programmatically
import codecs
import this

plain = codecs.decode(this.s, "rot_13")
assert "Beautiful is better than ugly." in plain
```

```python
# Goal: profile a callable without shelling out to python -m cProfile
import cProfile
import io

def target(n):
    return sum(range(n))

pr = cProfile.Profile()
pr.enable()
result = target(1000)
pr.disable()
stream = io.StringIO()
import pstats
pstats.Stats(pr, stream=stream).sort_stats("cumtime").print_stats()
assert result == 499500
assert "target" in stream.getvalue()
```

---

## Related CLI documentation

| Topic | Link |
|-------|------|
| Building your own CLI | [Command-line interface libraries](../command-line-interface-libraries/index.md) |
| Interpreter flags (`-m`, `-c`, `-O`, …) | [Command line — Python interpreter](https://docs.python.org/3/using/cmdline.html) |
| Profiling modules | [Debugging and Profiling](../debugging-and-profiling/index.md) |
| Codec registry (including `rot_13`) | [codecs](../binary-data-services/codecs-codec-registry-and-base-classes/index.md) |
