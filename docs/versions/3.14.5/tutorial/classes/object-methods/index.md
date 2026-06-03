# [Object Methods](https://docs.python.org/3/tutorial/classes.html#object-methods)

In this repo, **§9.4 — Object Methods** is grouped under [A First Look at Classes](../a-first-look-at-classes/index.md); see [Method Objects](../a-first-look-at-classes/method-objects/index.md) for the matching stub.

```python
# Bound vs unbound: functions on the class become bound methods when accessed on an instance.
class C:
    def f(self) -> int:
        return 1


c = C()
assert c.f() == 1 and type(C.f).__name__ in ("function", "method_descriptor")
```

Parent: [Classes](../index.md)
