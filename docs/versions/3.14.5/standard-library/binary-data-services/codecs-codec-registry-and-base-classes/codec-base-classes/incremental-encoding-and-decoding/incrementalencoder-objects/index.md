# [IncrementalEncoder Objects](https://docs.python.org/3/library/codecs.html#incrementalencoder-objects)

`codecs.IncrementalEncoder` is the base class for **chunked encoders**. Construct via `codecs.getincrementalencoder(encoding)(errors='strict')`. Each codec subclass implements `encode()` and inherits reset/state hooks. Specification on [docs.python.org](https://docs.python.org/3/library/codecs.html#incrementalencoder-objects).

---

## Constructor and attributes

| Member | Role |
|--------|------|
| `IncrementalEncoder(errors='strict')` | Standard constructor; extra kwargs allowed in subclasses |
| `.errors` | Active error handler name; assignable at runtime |

---

## Methods

| Method | Behavior |
|--------|----------|
| `encode(object, final=False)` | Encode chunk considering prior state; flush when `final=True` |
| `reset()` | Clear internal state; discard buffered output—call `encode('', final=True)` first if you need pending bytes |
| `getstate()` | Return an int (or encodable state) for persistence |
| `setstate(state)` | Restore from `getstate()` |

```python
# Goal: build output incrementally with explicit final flush
import codecs

enc = codecs.getincrementalencoder("utf-8")()
pieces = [enc.encode("Py"), enc.encode("thon", final=True)]
assert b"".join(pieces) == b"Python"
```

```python
# Goal: reset between messages on a long-lived encoder
import codecs

enc = codecs.getincrementalencoder("utf-8")()
enc.encode("first", final=True)
enc.reset()
out = enc.encode("second", final=True)
assert out == b"second"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Pass **`final=True`** once per logical message | Ensures trailing state is emitted |
| Read **`errors`** before long runs | `'replace'` vs `'strict'` changes output size |
| Prefer **`iterencode`** for simple iteration | Less boilerplate than manual encoder |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Calling `reset()` expecting prior output | Output is discarded—encode with `final=True` first |
| Reusing encoder after `final=True` without `reset` | State may be undefined—reset between messages |
| Using incremental encoder for **single-shot** data | Stateless `encode()` is simpler |
