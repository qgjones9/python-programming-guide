# [parameter](https://docs.python.org/3.14/glossary.html#term-parameter)

A named entity in a [function](../function/index.md) (or method) definition that specifies an [argument](../argument/index.md) (or in some cases, arguments) that the function can accept.  There are five kinds of parameter:

- *positional-or-keyword*: specifies an argument that can be passed either [positionally](../argument/index.md) or as a keyword argument.  This is the default kind of parameter, for example *foo* and *bar* in the following:

```python
def func(foo, bar=None): ...
```

- *positional-only*: specifies an argument that can be supplied only by position. Positional-only parameters can be defined by including a `/` character in the parameter list of the function definition after them, for example *posonly1* and *posonly2* in the following:

```python
def func(posonly1, posonly2, /, positional_or_keyword): ...
```

- *keyword-only*: specifies an argument that can be supplied only by keyword.  Keyword-only parameters can be defined by including a single var-positional parameter or bare `*` in the parameter list of the function definition before them, for example *kw_only1* and *kw_only2* in the following:

```python
def func(arg, *, kw_only1, kw_only2): ...
```

- *var-positional*: specifies that an arbitrary sequence of positional arguments can be provided (in addition to any positional arguments already accepted by other parameters).  Such a parameter can be defined by prepending the parameter name with `*`, for example *args* in the following:

```python
def func(*args, **kwargs): ...
```

- *var-keyword*: specifies that arbitrarily many keyword arguments can be provided (in addition to any keyword arguments already accepted by other parameters).  Such a parameter can be defined by prepending the parameter name with `**`, for example *kwargs* in the example above.

Parameters can specify both optional and required arguments, as well as default values for some optional arguments.

See also the [argument](../argument/index.md) glossary entry, the FAQ question on [the difference between arguments and parameters](https://docs.python.org/3.14/faq/programming.html#faq-argument-vs-parameter), the [inspect.Parameter](https://docs.python.org/3.14/library/inspect.html#inspect.Parameter) class, the [Function definitions](https://docs.python.org/3.14/reference/compound_stmts.html#function) section, and [PEP 362](https://peps.python.org/pep-0362/).
