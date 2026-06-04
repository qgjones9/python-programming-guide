# [configparser — Configuration file parser](https://docs.python.org/3/library/configparser.html)

The [`configparser`](https://docs.python.org/3/library/configparser.html) module implements an **INI-style** configuration language: named **sections** containing **key = value** pairs, similar to Windows INI files. Values are stored as strings; use typed getters for integers, floats, and booleans. A special **`DEFAULT`** section supplies fallback values for all other sections. Full interpolation, converters, and `ExtendedInterpolation` details remain on [docs.python.org](https://docs.python.org/3/library/configparser.html).

Related: [`tomllib`](../tomllib-parse-toml-files/index.md) for modern TOML config (e.g. `pyproject.toml`).

---

## Quick mental model — [Quick Start](https://docs.python.org/3/library/configparser.html#quick-start)

| Concept | Behavior |
|---------|----------|
| Sections | `[section.name]` headers; accessed like `config['section']` |
| Keys | Case-insensitive; stored lowercase |
| `DEFAULT` | Implicit defaults merged into every section |
| `read([files])` | Later files override earlier keys |
| Values | Always strings until `getint` / `getfloat` / `getboolean` |

```python
# Goal: build, write, and read an INI file
import configparser
import io

config = configparser.ConfigParser()
config["DEFAULT"] = {"Timeout": "30", "Debug": "no"}
config["app"] = {"Name": "demo", "Debug": "yes"}

buf = io.StringIO()
config.write(buf)
buf.seek(0)

loaded = configparser.ConfigParser()
loaded.read_file(buf)
assert loaded["app"]["name"] == "demo"
assert loaded["app"].getboolean("debug") is True
assert loaded["app"].getint("timeout") == 30  # inherited from DEFAULT
```

---

## Typed getters — [Supported Datatypes](https://docs.python.org/3/library/configparser.html#supported-datatypes)

| Method | Parses |
|--------|--------|
| `getint(section, option, ...)` | Integer literals |
| `getfloat(section, option, ...)` | Floating-point literals |
| `getboolean(section, option, ...)` | `yes`/`no`, `true`/`false`, `on`/`off`, `1`/`0` (case-insensitive) |

`bool("False")` is `True` in Python—never use bare `bool()` on config strings.

```python
# Goal: boolean getter recognizes common false tokens
import configparser

config = configparser.ConfigParser()
config.read_dict({"flags": {"enabled": "false", "verbose": "0", "trace": "off"}})
section = config["flags"]
assert section.getboolean("enabled") is False
assert section.getboolean("verbose") is False
assert section.getboolean("trace") is False
```

---

## Interpolation and overrides

| Feature | Use when |
|---------|----------|
| `BasicInterpolation` (default) | `%(key)s` references within same section |
| `ExtendedInterpolation` | Cross-section references like `%(path)s/logs` |
| Multiple `read()` files | Environment-specific overrides (dev vs prod) |

```python
# Goal: later config file overrides DEFAULT
import configparser
import io

base = io.StringIO("[DEFAULT]\nretries = 3\n")
override = io.StringIO("[DEFAULT]\nretries = 1\n")

cfg = configparser.ConfigParser()
cfg.read_file(base)
cfg.read_file(override)
assert cfg.getint("DEFAULT", "retries") == 1
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`getboolean` / `getint`** at boundaries | Avoid string-to-type bugs |
| Keep secrets **outside** INI or use env vars | Plain-text files are easy to leak |
| Prefer **TOML or env** for new projects | INI lacks nesting and has ambiguous typing |
| Document **`DEFAULT`** keys | Implicit inheritance surprises readers |
| Validate section names after `read()` | Missing section raises `KeyError` |
| Set **`allow_no_value=True`** only when needed | Supports flag-style keys without `=` |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `bool("False")` | Always true for non-empty string | Use `getboolean()` |
| `%` in values with default interpolation | `InterpolationSyntaxError` | Escape as `%%` or disable interpolation |
| Duplicate keys in one section | Last wins silently | Lint config files in CI |
| Expecting nested structures | INI is flat sections only | Use TOML/JSON/YAML for nesting |
| Writing Unicode paths on Windows | Encoding depends on `open` | Specify `encoding='utf-8'` |
| Relying on key case | Keys normalized to lowercase | Access with lowercase names |
