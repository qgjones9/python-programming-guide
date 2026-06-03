# [Constants added by the site module](https://docs.python.org/3/library/constants.html#constants-added-by-the-site-module)

The `site` module, which is automatically imported at interpreter startup (unless Python is started with the `-S` option), adds several helpful constants to the built-in namespace. These are intended for convenience in the interactive shell and **should not be used in production programs**.

### quit([code=None]) / exit([code=None])

- **Type:** Objects (can also be called as functions)
- **Interactive use:**  
  - When printed, they display a helpful message such as:  
    ```
    Use quit() or Ctrl-D (i.e. EOF) to exit
    ```
  - When called (e.g. `quit()` or `exit()`), they raise `SystemExit`, terminating the interpreter. An optional exit `code` can be provided.
- **Note:** In scripts or programs, use `sys.exit()` for exiting.

```python
# Interactive shell example
quit()
# Raises SystemExit and exits the interpreter
```

---

### help

- **Type:** Object
- **Interactive use:**  
  - When printed, shows:
    ```
    Type help() for interactive help, or help(object) for help about object.
    ```
  - When called as a function, enters the built-in help system (based on the `pydoc` module).

```python
help()
# Launches an interactive help utility.
help(str)
# Shows documentation for 'str' objects.
```

---

### copyright / credits

- **Type:** Objects
- **Interactive use:**  
  - When printed or called, display the copyright or credits for Python.

```python
print(copyright)
# Prints Python's copyright information.
credits
# Prints contributors to Python.
```

---

### license

- **Type:** Object
- **Interactive use:**  
  - When printed, shows:
    ```
    Type license() to see the full license text
    ```
  - When called as a function, displays the complete Python license in a pager for easier reading (one screen at a time).

```python
license
# Prints a prompt to call license()
license()
# Shows the full license text interactively.
```

---

**Summary Table**

| Name      | Purpose                                                         | Typical Use               |
|-----------|-----------------------------------------------------------------|---------------------------|
| quit(), exit() | Exit the interactive interpreter (raise SystemExit)         | Interactive sessions only |
| help      | Start interactive help / show object help                       | Interactive sessions only |
| copyright | Show Python copyright information                               | Interactive sessions only |
| credits   | Show contributors to Python                                     | Interactive sessions only |
| license   | Show instructions or the full license text                      | Interactive sessions only |

> These constants are available only after the `site` module is imported (which is the default). They **should not be relied upon in scripts**; use standard libraries like `sys` and `pydoc` instead if needed in programs.