# [Comments](https://docs.python.org/3/reference/lexical_analysis.html#comments)

In Python, you create a comment by starting a line (or part of a line) with the hash character (`#`). Anything following the `#` on that line is considered a comment and is ignored by the Python interpreter—it will not affect how your code runs.

It's important to note that a comment must not be part of a string literal; only a standalone `#` (outside of quotes) is recognized as starting a comment. The comment extends all the way to the end of the physical line.

When you place a comment on a line, it marks the logical end of a statement on that line, unless you are using the implicit line joining rules, such as when you're inside parentheses, brackets, or braces. In those cases, comments can appear in the middle of a logical line, and Python will still correctly interpret your code.

In summary, comments are meant for humans to read—they help explain and document your code, but they are completely ignored by Python's syntax rules during execution.

```python
# This is a comment
print("Hello, World!")  # This is also a comment
```

```python
print("Hello, World!")  # This is a comment
print("Hello, World!")  # This is a comment
```
