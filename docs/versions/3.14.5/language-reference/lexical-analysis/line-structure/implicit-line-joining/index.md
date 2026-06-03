# [Implicit line joining](https://docs.python.org/3/reference/lexical_analysis.html#implicit-line-joining)

When you write an expression that is inside parentheses `()`, square brackets `[]`, or curly braces `{}`, you can break it across multiple lines without needing a backslash. This makes it easy to write long lists, dictionaries, or function arguments for better readability. For example:

```python
numbers = [
    1, 2, 3,    # first three numbers
    4, 5, 6,    # next three numbers
    7, 8, 9     # last three numbers
]
```

You can add comments to these continued lines, and the amount of indentation does not matter. You may also include blank lines. Python treats all the lines inside the matching brackets, braces, or parentheses as a single logical line. For example:

```python
numbers = [
    1, 2, 3,    # first three numbers

    4, 5, 6,    # next three numbers
    
    7, 8, 9     # last three numbers
]
print(numbers)  # This will run and the blank lines are fine
# Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

If you use triple-quoted strings that span multiple lines, you can also continue over several lines, but you cannot include comments in the middle of such a string.

```python
message = """
This is a multi-line string.
It can continue over several lines.
"""
print(message)  # This will run and the blank lines are fine
# Output: This is a multi-line string.
# It can continue over several lines.
```


