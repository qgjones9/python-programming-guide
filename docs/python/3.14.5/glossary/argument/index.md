# [argument](https://docs.python.org/3.14/glossary.html#term-argument)

A value passed to a [function](../function/index.md) (or [method](../method/index.md)) when calling the
function.  There are two kinds of argument:

- *keyword argument*: an argument preceded by an identifier (e.g.
`name=`) in a function call or passed as a value in a dictionary
preceded by `**`.  For example, `3` and `5` are both keyword
arguments in the following calls to [complex()](https://docs.python.org/3.14/library/functions.html#complex):

```python
complex(real=3, imag=5)
complex(**{'real': 3, 'imag': 5})
```

- *positional argument*: an argument that is not a keyword argument.
Positional arguments can appear at the beginning of an argument list
and/or be passed as elements of an [iterable](../iterable/index.md) preceded by `*`.
For example, `3` and `5` are both positional arguments in the
following calls:

```python
complex(3, 5)
complex(*(3, 5))
```

Arguments are assigned to the named local variables in a function body.
See the [Calls](https://docs.python.org/3.14/reference/expressions.html#calls) section for the rules governing this assignment.
Syntactically, any expression can be used to represent an argument; the
evaluated value is assigned to the local variable.

See also the [parameter](../parameter/index.md) glossary entry, the FAQ question on
[the difference between arguments and parameters](https://docs.python.org/3.14/faq/programming.html#faq-argument-vs-parameter), and [PEP 362](https://peps.python.org/pep-0362/).
