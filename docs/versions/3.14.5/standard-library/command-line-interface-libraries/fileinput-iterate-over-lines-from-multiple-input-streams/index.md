# [fileinput — Iterate over lines from multiple input streams](https://docs.python.org/3/library/fileinput.html)

The [`fileinput`](https://docs.python.org/3/library/fileinput.html) module helps write **Unix-filter-style** loops over **multiple files** and **`stdin`**. The usual pattern is `for line in fileinput.input(): ...`, which walks `sys.argv[1:]` (or a list you pass), treats `'-'` as stdin, and exposes helpers like `filename()` and `lineno()`. Full API remains on [docs.python.org](https://docs.python.org/3/library/fileinput.html).

---

## Primary API — [fileinput.input()](https://docs.python.org/3/library/fileinput.html#fileinput.input)

| Parameter | Role |
|-----------|------|
| `files=None` | Sequence of paths; default `sys.argv[1:]` or stdin if empty |
| `inplace=False` | Write stdout back into each file (backup optional) |
| `backup='.bak'` | Extension for backup when `inplace=True` |
| `encoding` / `errors` | Passed to `open()` (3.10+) |
| `openhook` | Custom opener (e.g. gzip/bz2) |

```python
# Goal: iterate explicit file list with encoding
import fileinput
import tempfile
import os

lines = []
with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
    f.write("alpha\nbeta\n")
    path = f.name

try:
    with fileinput.input(files=[path], encoding="utf-8") as fi:
        for line in fi:
            lines.append(line.rstrip("\n"))
    assert lines == ["alpha", "beta"]
finally:
    os.unlink(path)
```

---

## Global state helpers

After `input()` starts iteration, module-level functions reflect the **current** file:

| Function | Returns |
|----------|---------|
| `filename()` | Path of file being read (`None` before first line) |
| `lineno()` | Cumulative line number across all files |
| `filelineno()` | Line number within current file |
| `isfirstline()` | `True` if line is first in its file |
| `isstdin()` | `True` if reading `sys.stdin` |
| `nextfile()` | Close current file early, skip to next |
| `close()` | End the sequence |

```python
# Goal: lineno and isfirstline across two temp files
import fileinput
import tempfile
import os

paths = []
for content in ("a\n", "b\nc\n"):
    tf = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False)
    tf.write(content)
    tf.close()
    paths.append(tf.name)

try:
    records = []
    with fileinput.input(files=paths, encoding="utf-8") as fi:
        for line in fi:
            records.append((fileinput.filename(), fileinput.filelineno(), fileinput.isfirstline()))
    assert records[0][2] is True   # first line of file 1
    assert records[1][2] is True   # first line of file 2
    assert records[2][2] is False  # second line of file 2
finally:
    for p in paths:
        os.unlink(p)
```

---

## Compressed files — [hook_compressed](https://docs.python.org/3/library/fileinput.html#fileinput.hook_compressed)

`openhook=fileinput.hook_compressed` transparently opens `.gz` and `.bz2` files.

```python
# Goal: read a .gz file via hook_compressed
import fileinput
import gzip
import tempfile
import os

data = b"hello gzip\n"
with tempfile.NamedTemporaryFile(suffix=".gz", delete=False) as f:
    f.write(gzip.compress(data))
    path = f.name

try:
    with fileinput.input(files=[path], openhook=fileinput.hook_compressed, encoding="utf-8") as fi:
        text = "".join(fi)
    assert "hello gzip" in text
finally:
    os.unlink(path)
```

---

## In-place editing

With `inplace=True`, stdout is redirected into the current input file; a backup file is created unless `backup=''`.

```python
# Goal: uppercase a file in place with backup
import fileinput
import tempfile
import os

with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
    f.write("lower\n")
    path = f.name
bak = path + ".bak"

try:
    with fileinput.input(files=[path], inplace=True, backup=".bak", encoding="utf-8") as fi:
        for line in fi:
            print(line.upper(), end="")
    with open(path, encoding="utf-8") as f:
        assert f.read() == "LOWER\n"
    assert os.path.exists(bak)
finally:
    for p in (path, bak):
        if os.path.exists(p):
            os.unlink(p)
```

---

## Context manager and class

`FileInput` mirrors `input()` and supports `with` blocks (3.2+). Prefer explicit `encoding="utf-8"` for portable text tools.

```python
# Goal: FileInput as context manager
import fileinput
import io

buf = io.StringIO("x\ny\n")
# FileInput expects filenames; use a real temp file pattern in apps.
# Here we verify the class is iterable and exposes readline.
import tempfile, os
with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
    f.write("only\n")
    p = f.name
try:
    with fileinput.FileInput(files=[p], encoding="utf-8") as inp:
        assert inp.readline() == "only\n"
        assert inp.readline() == ""
finally:
    os.unlink(p)
```
