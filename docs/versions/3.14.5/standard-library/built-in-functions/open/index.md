# [open()](https://docs.python.org/3/library/functions.html#open)

## Description

`open(file, mode='r', encoding=None, ...)` returns a file object. Text mode (default) decodes bytes to `str`; binary mode (`'rb'`, `'wb'`) works with `bytes`. Context managers (`with open(...)`) ensure files close reliably.

## What problem it solves

Reading configuration, writing logs, and processing data on disk—the primary interface between Python programs and the filesystem.

## Implementation options

### Read a text file

```python
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "sample.txt"
    path.write_text("line1\nline2\n", encoding="utf-8")
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines == ["line1", "line2"]
```

### Write binary data

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "data.bin"
    with open(path, "wb") as f:
        f.write(bytes([0, 255, 128]))
    assert path.read_bytes() == bytes([0, 255, 128])
```

### Exclusive create with mode x

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "new.txt"
    with open(path, "x", encoding="utf-8") as f:
        f.write("created")
    try:
        open(path, "x", encoding="utf-8")
        created_twice = True
    except FileExistsError:
        created_twice = False
    assert not created_twice
```

## Best practices

- Always use `with open(...)` so files close even when exceptions occur.

  ```python
  import tempfile
  from pathlib import Path

  with tempfile.TemporaryDirectory() as tmp:
      path = Path(tmp) / "data.txt"
      with open(path, "w", encoding="utf-8") as f:
          f.write("ok")
      assert path.read_text(encoding="utf-8") == "ok"
  ```

  ```python
  # Incorrect—file may stay open if an exception occurs before close():
  # f = open(path)
  # f.write("ok")
  # f.close()
  ```

- Specify `encoding="utf-8"` for text files when portability matters.

  ```python
  import tempfile
  from pathlib import Path

  with tempfile.TemporaryDirectory() as tmp:
      path = Path(tmp) / "utf8.txt"
      with open(path, "w", encoding="utf-8") as f:
          f.write("café")
      with open(path, encoding="utf-8") as f:
          assert f.read() == "café"
  ```

  ```python
  # Incorrect on non-UTF-8 systems—locale default may mangle Unicode:
  # open(path, "w").write("café")
  ```

- Use `pathlib.Path.read_text` / `write_text` for small files when convenience beats fine-grained control.

  ```python
  import tempfile
  from pathlib import Path

  with tempfile.TemporaryDirectory() as tmp:
      path = Path(tmp) / "small.txt"
      path.write_text("hello", encoding="utf-8")
      assert path.read_text(encoding="utf-8") == "hello"
  ```

  ```python
  # open() is better when you need streaming or binary chunk I/O:
  # with open(large_path, "rb") as f:
  #     chunk = f.read(1024)
  ```
