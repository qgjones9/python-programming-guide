# [input()](https://docs.python.org/3/library/functions.html#input)

## Description

Reads a line from standard input as a string, optionally writing a prompt to stdout first.

## What problem it solves

Command-line tools and interactive scripts need to collect user text without pulling in a full GUI or web form.

## Implementation options

### Option 1: Read a line with `input()` using redirected stdin

```python
import io
import sys

def read_line_with_prompt(prompt: str, typed: str) -> str:
    original = sys.stdin
    sys.stdin = io.StringIO(typed + "\n")
    try:
        return input(prompt)
    finally:
        sys.stdin = original

answer = read_line_with_prompt("Name: ", "Ada")
assert answer == "Ada"
```

### Option 2: Parse numeric input after `input()`

```python
import io
import sys

def read_age(prompt: str, typed: str) -> int:
    original = sys.stdin
    sys.stdin = io.StringIO(typed + "\n")
    try:
        return int(input(prompt).strip())
    finally:
        sys.stdin = original

assert read_age("Enter your age: ", "  42  ") == 42
```

### Option 3: Validate yes/no responses

```python
def normalize_yes_no(text: str) -> bool:
    answer = text.strip().lower()
    if answer in {"y", "yes"}:
        return True
    if answer in {"n", "no"}:
        return False
    raise ValueError("expected yes or no")

assert normalize_yes_no("  YES  ") is True
assert normalize_yes_no("no") is False
```

### Option 4: Split comma-separated input

```python
import io
import sys

def read_tags(prompt: str, typed: str) -> list[str]:
    original = sys.stdin
    sys.stdin = io.StringIO(typed + "\n")
    try:
        line = input(prompt)
    finally:
        sys.stdin = original
    return [part.strip() for part in line.split(",") if part.strip()]

assert read_tags("Tags: ", " python, asyncio , ") == ["python", "asyncio"]
```

## Best practices

- Always validate and convert `input()` results; it always returns a string.

  ```python
  import io
  import sys

  def read_age(prompt: str, typed: str) -> int:
      original = sys.stdin
      sys.stdin = io.StringIO(typed + "\n")
      try:
          return int(input(prompt).strip())
      finally:
          sys.stdin = original

  assert read_age("Age: ", "  42  ") == 42
  ```

- Wrap conversion in `try/except ValueError` for robust CLI tools.

  ```python
  def parse_int(text: str) -> int | None:
      try:
          return int(text.strip())
      except ValueError:
          return None

  assert parse_int("42") == 42
  assert parse_int("nope") is None
  ```

- Treat empty lines and whitespace explicitly; `input()` does not strip for you.

  ```python
  import io
  import sys

  def read_name(prompt: str, typed: str) -> str:
      original = sys.stdin
      sys.stdin = io.StringIO(typed + "\n")
      try:
          return input(prompt).strip()
      finally:
          sys.stdin = original

  assert read_name("Name: ", "  Ada  ") == "Ada"
  assert read_name("Name: ", "") == ""
  ```
