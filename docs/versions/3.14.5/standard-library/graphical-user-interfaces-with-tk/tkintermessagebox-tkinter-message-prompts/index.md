# [tkinter.messagebox — Tkinter message prompts](https://docs.python.org/3/library/tkinter.messagebox.html)

**`tkinter.messagebox`** provides modal message windows—information, warning, error, and question styles—with platform-native button sets. Functions block until the user chooses, then return symbolic button names or booleans. Canonical docs: [tkinter.messagebox.html](https://docs.python.org/3/library/tkinter.messagebox.html).

---

## Return values

| Function family | Typical return |
|-----------------|----------------|
| **`showinfo`**, **`showwarning`**, **`showerror`** | `"ok"` (informational) |
| **`askokcancel`**, **`askretrycancel`**, **`askyesno`** | `True` / `False` |
| **`askyesnocancel`** | `True` / `False` / `None` (cancel) |
| **`askquestion`** | `"yes"` / `"no"` |

Symbolic button names: **`OK`**, **`CANCEL`**, **`YES`**, **`NO`**, **`RETRY`**, **`ABORT`**, **`IGNORE`**.

---

### Message class — [Message](https://docs.python.org/3/library/tkinter.messagebox.html#tkinter.messagebox.Message)

| Option | Role |
|--------|------|
| **`message`** | Primary text |
| **`detail`** | Secondary, less emphasized line (where supported) |
| **`title`** | Window title (ignored on macOS for this dialog type) |
| **`icon`** | `ERROR`, `INFO`, `QUESTION`, `WARNING` |
| **`type`** | Button set: `OK`, `OKCANCEL`, `YESNO`, `YESNOCANCEL`, … |
| **`default`** | Symbolic name of default button |
| **`parent`** | Logical parent window |

Call **`show(**options)`** to display; kwargs override constructor options.

---

### Convenience functions

| Function | Button set |
|----------|------------|
| **`showinfo(title, message, **options)`** | OK |
| **`showwarning(title, message, **options)`** | OK |
| **`showerror(title, message, **options)`** | OK |
| **`askquestion(title, message, *, type=YESNO, **options)`** | YES / NO |
| **`askokcancel(title, message, **options)`** | OK / CANCEL |
| **`askretrycancel(title, message, **options)`** | RETRY / CANCEL |
| **`askyesno(title, message, **options)`** | YES / NO |
| **`askyesnocancel(title, message, **options)`** | YES / NO / CANCEL |

```python
# Goal: map askyesno-style results to actions without a GUI
def action_for_yesno(answer, on_yes, on_no):
    if answer:
        return on_yes()
    return on_no()

assert action_for_yesno(True, lambda: "saved", lambda: "discarded") == "saved"
assert action_for_yesno(False, lambda: "saved", lambda: "discarded") == "discarded"
```

```python
# Goal: confirm before delete (illustrative — requires tkinter + display)
# from tkinter import Tk
# from tkinter.messagebox import askyesno, showerror
# root = Tk()
# root.withdraw()
# if askyesno("Confirm", "Delete this item?", parent=root):
#     pass  # perform delete
# else:
#     showerror("Cancelled", "Nothing was deleted.", parent=root)
# root.destroy()
assert True
```

---

### Constants — button sets and icons

| Constant | Value / meaning |
|----------|-----------------|
| **`OK`**, **`OKCANCEL`**, **`YESNO`**, **`YESNOCANCEL`**, **`RETRYCANCEL`**, **`ABORTRETRYIGNORE`** | Predefined **`type`** layouts |
| **`ERROR`**, **`INFO`**, **`QUESTION`**, **`WARNING`** | Standard icons |

---

## Best practices

| Practice | Why |
|----------|-----|
| Pass **`parent=root`** | Keeps dialog above your app; correct modality |
| Use **`askyesno`** for destructive confirms | Clear boolean API |
| Use **`askyesnocancel`** when cancel must mean “do nothing” | Distinguish No from Cancel |
| Avoid **`showinfo`** for errors | Use **`showerror`** so icon matches severity |
| Do not block network threads | Call message boxes only from the GUI thread |

---

## See also

- [Tkinter Dialogs](../tkinter-dialogs/index.md) — `commondialog` base
- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — event loop and `withdraw()`
