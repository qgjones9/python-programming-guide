# [Blank lines](https://docs.python.org/3/reference/lexical_analysis.html#blank-lines)

In Python, blank lines are lines that contain only whitespace characters (such as spaces, tabs, or formfeed characters) or optional comments and no other code. These lines are completely ignored by the Python parser; they do not generate a NEWLINE token and do not affect how your code runs.

When you are entering code in the interactive interpreter, the way blank lines are handled may depend on the specific implementation you are using. In the standard Python interactive shell, typing a truly blank line (with no spaces, tabs, or comments) will end a multi-line statement and tell the interpreter to execute the block. Blank lines that contain only whitespace or a comment are simply skipped and do not end the statement.
  
For example, in a function definition or a block, you can insert blank lines for clarity, and Python will ignore them:

```python
def my_function():
    print("Hello")

    # This is a blank line above, and a comment here
    print("World")
```

So, use blank lines to make your code more readable—they won’t interfere with how Python interprets your code.