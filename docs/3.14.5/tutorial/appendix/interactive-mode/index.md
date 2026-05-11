# [Interactive Mode](https://docs.python.org/3/tutorial/appendix.html#interactive-mode)

Condensed notes for **§16.1** in the [Appendix](https://docs.python.org/3/tutorial/appendix.html): how the interpreter behaves on errors in the REPL, how to make scripts executable on Unix, **`PYTHONSTARTUP`**, and **`sitecustomize` / `usercustomize`**.

```python
import site

# `site` controls per-user `site-packages` discovery and optional startup customization.
assert hasattr(site, "USER_SITE")
```

## Sections in this repo

- [Error Handling](error-handling/index.md)
- [Executable Python Scripts](executable-python-scripts/index.md)
- [The Interactive Startup File](the-interactive-startup-file/index.md)
- [The Customization Modules](the-customization-modules/index.md)

Parent: [Appendix](../index.md)
