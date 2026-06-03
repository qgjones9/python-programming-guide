# [type alias](https://docs.python.org/3.14/glossary.html#term-type-alias)

A synonym for a type, created by assigning the type to an identifier.

Type aliases are useful for simplifying [type hints](../type-hint/index.md). For example:

```python
def remove_gray_shades(
        colors: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    pass
```

could be made more readable like this:

```python
Color = tuple[int, int, int]

def remove_gray_shades(colors: list[Color]) -> list[Color]:
    pass
```

See [typing](https://docs.python.org/3.14/library/typing.html#module-typing) and [PEP 484](https://peps.python.org/pep-0484/), which describe this functionality.

