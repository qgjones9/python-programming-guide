# [breakpoint()](https://docs.python.org/3/library/functions.html#breakpoint)

## Description

`breakpoint()` drops into a debugger at the call site by invoking `sys.breakpointhook()`, which defaults to `pdb.set_trace()`. Extra positional and keyword arguments are forwarded to the hook (Python 3.7+).

## What problem it solves

Temporary debugging should be fast to add and remove. `breakpoint()` avoids importing `pdb` and keeps a single hook point you can redirect—useful for IDE debuggers, remote hooks, or disabling breakpoints via `PYTHONBREAKPOINT=0`.

## Implementation options

### Basic inspection (interactive)

```python
def divide(a, b):
    # breakpoint()  # uncomment to inspect a, b before division
    return a / b

assert divide(10, 2) == 5.0
```

### Custom hook for tests or CI

```python
import sys

def log_hook(*args, **kwargs):
    print("debug hook:", args, kwargs)

sys.breakpointhook = log_hook
breakpoint("paused", reason="demo")  # prints instead of entering pdb
sys.breakpointhook = sys.__breakpointhook__  # restore default
```

## Best practices

- Remove or guard breakpoints before shipping; set `PYTHONBREAKPOINT=0` in production to disable them.
- Replace `import pdb; pdb.set_trace()` with `breakpoint()` for consistency and hook compatibility.
- Do not rely on `breakpoint()` in automated tests—it blocks on stdin unless the hook is overridden.
