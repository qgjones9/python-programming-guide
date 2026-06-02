# [Python Scopes and Namespaces](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)

Condensed notes for **§9.2** of [Classes](https://docs.python.org/3/tutorial/classes.html): how namespaces are created for modules, functions, classes, and instances, and how **LEGB** resolution interacts with **`global`** / **`nonlocal`**.

```python
x = "global"

def demo():
    x = "local"
    return x


assert demo() == "local" and x == "global"  # inner assignment does not mutate the global name
```

## Sections in this repo

- [Scopes and Namespaces Example](scopes-and-namespaces-example/index.md)

Parent: [Classes](../index.md)
