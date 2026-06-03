# [Pythonic](https://docs.python.org/3.14/glossary.html#term-Pythonic)

An idea or piece of code which closely follows the most common idioms of the Python language, rather than implementing code using concepts common to other languages.  For example, a common idiom in Python is to loop over all elements of an iterable using a [for](https://docs.python.org/3.14/reference/compound_stmts.html#for) statement.  Many other languages don’t have this type of construct, so people unfamiliar with Python sometimes use a numerical counter instead:

```python
for i in range(len(food)):
    print(food[i])
```

As opposed to the cleaner, Pythonic method:

```python
for piece in food:
    print(piece)
```

