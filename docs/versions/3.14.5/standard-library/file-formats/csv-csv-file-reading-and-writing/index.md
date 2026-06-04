# [csv — CSV File Reading and Writing](https://docs.python.org/3/library/csv.html)

The [`csv`](https://docs.python.org/3/library/csv.html) module reads and writes **tabular data** in Comma Separated Values and related dialects. It hides Excel-specific quoting rules while letting you register custom dialects. Rows are sequences (lists) or dicts (`DictReader` / `DictWriter`); no automatic type conversion unless `QUOTE_NONNUMERIC` is set. Full dialect and quoting matrices remain on [docs.python.org](https://docs.python.org/3/library/csv.html).

---

## Core API — [Module Contents](https://docs.python.org/3/library/csv.html#module-csv)

| Function / class | Role |
|------------------|------|
| `reader(csvfile, dialect='excel', **fmtparams)` | Iterate rows as lists of strings |
| `writer(csvfile, dialect='excel', **fmtparams)` | Write rows from sequences |
| `DictReader(f, fieldnames=None, ...)` | Map each row to a `dict` keyed by column names |
| `DictWriter(f, fieldnames, ...)` | Write dict rows in column order |
| `register_dialect` / `get_dialect` / `list_dialects` | Named reusable format profiles |
| `field_size_limit([new_limit])` | Cap or query max parsed field width |

Open file objects with **`newline=''`** so the module controls line endings.

---

## Dialects and quoting — [Dialects and Formatting Parameters](https://docs.python.org/3/library/csv.html#dialects-and-formatting-parameters)

| Parameter | Typical value | Effect |
|-----------|---------------|--------|
| `delimiter` | `','` | Field separator |
| `quotechar` | `'"'` | Character wrapping fields with special chars |
| `quoting` | `QUOTE_MINIMAL` | When to add quotes (`QUOTE_ALL`, `QUOTE_NONNUMERIC`, `QUOTE_NONE`) |
| `lineterminator` | `'\r\n'` | Row terminator on write |
| `skipinitialspace` | `False` | Strip whitespace after delimiter |

Built-in dialect names include **`excel`**, **`excel-tab`**, and **`unix`**.

```python
# Goal: write and read CSV with a custom delimiter
import csv
import io

buf = io.StringIO()
writer = csv.writer(buf, delimiter="|", quotechar="'", quoting=csv.QUOTE_MINIMAL)
writer.writerow(["a", "b", "c"])
writer.writerow(["x", "y"])
buf.seek(0)
rows = list(csv.reader(buf, delimiter="|", quotechar="'"))
assert rows == [["a", "b", "c"], ["x", "y"]]
```

```python
# Goal: DictReader preserves header keys
import csv
import io

text = "id,name\n1,alice\n2,bob\n"
reader = csv.DictReader(io.StringIO(text))
rows = list(reader)
assert rows[0]["id"] == "1" and rows[1]["name"] == "bob"
```

```python
# Goal: DictWriter with explicit field order
import csv
import io

buf = io.StringIO()
fields = ["name", "qty"]
writer = csv.DictWriter(buf, fieldnames=fields)
writer.writeheader()
writer.writerow({"name": "apple", "qty": "12"})
buf.seek(0)
assert "apple" in buf.read()
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Always `open(..., newline='')` | Prevents `\r\r\n` artifacts on Windows |
| Use **`DictReader`** for header rows | Avoids magic column indexes |
| Register a **dialect** for repeated formats | Keeps reader/writer parameters in sync |
| Treat all fields as **strings** by default | Cast explicitly after read |
| Set **`extrasaction='ignore'`** on DictWriter when dicts may have extra keys | Avoids `ValueError` on unknown keys |
| Increase **`field_size_limit`** only when needed | Default protects against huge fields |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Missing `newline=''` | Embedded `\r` in fields | Document and enforce open flags |
| `QUOTE_NONE` with delimiter in data | `Error` on write | Enable quoting or escape manually |
| Assuming RFC 4180 everywhere | Vendor-specific quirks | Test against producer application |
| `None` in SQL export | Written as empty string (irreversible) | Document NULL handling |
| Mixing `utf-8` and locale encoding | Mojibake | Pass explicit `encoding=` to `open` |
| Very wide rows | `Error: field larger than limit` | Call `csv.field_size_limit()` judiciously |
