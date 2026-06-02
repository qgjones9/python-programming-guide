# [Indentation](https://docs.python.org/3/reference/lexical_analysis.html#indentation)

In Python, indentation—the number of spaces or tabs at the start of a line—tells the interpreter how statements are grouped. Indentation determines what code belongs to a block, like inside an `if`, `for`, or function definition.

**How indentation works:**

- You may use spaces or tabs for indentation, but **do not mix spaces and tabs** within the same block—if Python detects ambiguous or inconsistent mixing, it raises a [TabError](../../../../../standard-library/built-in-exceptions/concrete-exceptions/index.md#taberror).
- Tabs count as enough spaces so the total before your first code character is a multiple of eight, which matches what Unix editors do. But, for simplicity and best practice, just use spaces consistently.
- You cannot break the indentation part of a line across more than one physical line by using a backslash.
- Most editors will work fine if you stick to spaces, but using a mix of tabs and spaces can cause trouble, especially if you move your code between different computers or editors.
- If a line starts with a "formfeed" character (a rare whitespace character), it's ignored for indentation.

**How Python uses indentation to track blocks:**

Python uses indentation to mark the start and end of blocks of code. When the indentation increases compared to the previous line, Python knows you've started a new block (like under an [if](../../../../language-reference/compound-statements/the-if-statement/index.md) or [for](../../../../language-reference/compound-statements/the-for-statement/index.md)). When the indentation goes back to an earlier level, Python knows that block has ended.

**A simple example of correct indentation:**

```python
def greet(name):
    if name:
        print("Hello,", name)
    print("Done")
```

In this example:`
- The `print("Hello,", name)` line is indented under the `if name:`, so it's only run if `name` is true.
- The second `print("Done")` line lines up with the start of the `if`, so it's always run after the check.

**Examples of indentation errors:**

Here are some ways indentation can go wrong:

```python
 def greet(name):        # error: unexpected space at the start
print("Hello,", name)    # error: should be indented under function
    print("Done")        # error: indentation doesn't match block structure
```

If your indentation jumps around unpredictably, or mixes tabs and spaces wrongly, Python will give errors to help you fix it.

Remember: stick to a consistent style (spaces are recommended), and let your editor help you by showing indentation clearly.