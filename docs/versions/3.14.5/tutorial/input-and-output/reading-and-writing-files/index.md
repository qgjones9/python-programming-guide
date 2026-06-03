# [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)

Condensed notes for **§7.2** of [Input and Output](https://docs.python.org/3/tutorial/inputoutput.html): **`open`**, text vs binary modes, **`read` / `readline` / `write`**, and **`Path`**-based workflows on modern codebases.

```python
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "sample.txt"
    p.write_text("hello\n", encoding="utf-8")
    # `read_text` decodes bytes to str using the declared encoding.
    assert p.read_text(encoding="utf-8") == "hello\n"
```

## Sections in this repo

- [Methods of File Objects](methods-of-file-objects/index.md)
- [Saving structured data with json](saving-structured-data-with-json/index.md)

Parent: [Input and Output](../index.md)
