# [input()](https://docs.python.org/3/library/functions.html#input)

## Description

Reads a line from standard input as a string, optionally writing a prompt to stdout first.

## What problem it solves

Command-line tools and interactive scripts need to collect user text without pulling in a full GUI or web form.

## Implementation options

### Option 1: Prompt and parse numeric input (pattern)

```python
# Interactive REPL usage:
# age = int(input("Enter your age: "))

def parse_positive_int(text: str) -> int:
    value = int(text.strip())
    if value <= 0:
        raise ValueError("must be positive")
    return value

assert parse_positive_int("  42\n") == 42
```

### Option 2: Validate yes/no responses

```python
def normalize_yes_no(text: str) -> bool:
    answer = text.strip().lower()
    if answer in {"y", "yes"}:
        return True
    if answer in {"n", "no"}:
        return False
    raise ValueError("expected yes or no")

assert normalize_yes_no("  YES  ") is True
```

## Best practices

- Always validate and convert `input()` results; it always returns a string.
- Wrap conversion in `try/except ValueError` for robust CLI tools.
- When the readline module is available, users get line editing and history in the terminal.
