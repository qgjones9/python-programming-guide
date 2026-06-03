# [Explicit line joining](https://docs.python.org/3/reference/lexical_analysis.html#explicit-line-joining)

In Python, you can explicitly continue a statement across multiple physical lines using the backslash character (`\`). If a line ends with a backslash (and the backslash is not inside a string literal or comment), Python will join that line with the one that follows, treating them as a single logical line. The backslash itself and the newline character immediately after it are ignored by the interpreter. Here’s how it works:


```python
print("Hello, World!") \
    + "This is a test" 
```

This is equivalent to:

```python
print("Hello, World!This is a test")
``` 



## Rules and limits

The backslash join is powerful, but only in specific places. These rules keep the tokenizer from misreading your source.

### No comment after a joining backslash

If `\` is meant to continue the line, nothing may follow it on that physical line—not even a comment.

```python
# Invalid — the comment is on the same line as the join
total = 1 + 2 \  # add the next line
    + 3
```

Put the comment on the next line instead, or drop it from the continuation line.

### A backslash does not continue a comment

A `\` at the end of a **comment** line does not join the next line into that comment. The next line is normal code.

```python
# This comment ends here \
x = 1   # this runs — it is not part of the comment above
```

### Only string literals may split a token with `\`

You can break a **string literal** across lines with a backslash inside the quotes. You **cannot** break other tokens—such as a number, name, or operator—across lines that way.

```python
# Valid — backslash inside the string literal
message = "The quick brown fox \
jumps over the lazy dog"

# Invalid — the name is split across lines (SyntaxError)
my_var \
iable = 10

# Invalid — the operator is split (SyntaxError)
x = 1 \
+ 2
```

For non-string code, put the `\` **between** tokens (as in the example at the top of this page), not in the middle of one token.

### `\` is only special at the end of a line (outside strings)

Outside string literals, a backslash in the **middle** of a line is not a line-joiner—it is a syntax error unless it starts a valid escape inside a string.

```python
# Invalid — backslash in the middle of the line (SyntaxError)
x = 1 \ + 2

# Valid — backslash at end of line joins the next physical line
x = 1 \
    + 2
```

Inside a string, `\` still means escape or continuation as usual:

```python
path = "C:\\Users\\name"   # escaped backslashes inside the literal
```
