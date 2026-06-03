# [Ignored end of line](https://docs.python.org/3/reference/lexical_analysis.html#ignored-end-of-line)


If you place a backslash (`\`) at the end of a line in a string literal, Python ignores the newline, treating it as if the string continues uninterrupted. For example:

```python
message = 'This string is written on two lines \
but results in a single line.'
print(message)
# Output: This string is written on two lines but results in a single line.
```

This technique can be useful for breaking up long string literals for readability. You can achieve the same effect by using triple-quoted strings or by implicitly concatenating multiple string literals within parentheses.

```python
# Triple-quoted string (preserves newlines unless you remove them)
text = """This string
spans multiple lines."""
# Implicit concatenation removes need for backslashes
msg = (
    "This is a very long string "
    "split over multiple lines, "
    "but is combined into one."
)
```
