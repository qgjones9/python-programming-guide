# [qualified name](https://docs.python.org/3.14/glossary.html#term-qualified-name)

A dotted name showing the “path” from a module’s global scope to a
class, function or method defined in that module, as defined in
[PEP 3155](https://peps.python.org/pep-3155/).  For top-level functions and classes, the qualified name
is the same as the object’s name:

```python
>>> class C:
...     class D:
...         def meth(self):
...             pass
...
>>> C.__qualname__
'C'
>>> C.D.__qualname__
'C.D'
>>> C.D.meth.__qualname__
'C.D.meth'
```

When used to refer to modules, the *fully qualified name* means the
entire dotted path to the module, including any parent packages,
e.g. `email.mime.text`:

```python
>>> import email.mime.text
>>> email.mime.text.__name__
'email.mime.text'
```
