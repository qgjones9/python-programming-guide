# Trie collect walkthrough

This README traces `collect()` line by line so you can see exactly what the
code does. Start with a trie that already stores **cat**, **car**, and **coat**.

## Starting trie

After:

```python
trie = Trie()
trie.insert("cat")
trie.insert("car")
trie.insert("coat")
```

`len(trie)` is **3**. The tree looks like this (`*` = word end):

```text
root
└─ c
   ├─ a
   │  ├─ r *          ← "car"
   │  └─ t *          ← "cat"
   └─ o
      └─ a
         └─ t *       ← "coat"
```

Shared idea: `collect(prefix)` does two phases.

| phase | method | job |
|-------|--------|-----|
| 1 — navigate | `_find_node(prefix)` | Walk the trie character by character. Return the node at the end of the prefix, or `None` if any edge is missing. |
| 2 — enumerate | `_dfs_words(node, parts, out)` | Depth-first search from that node. Every time a node has `is_end = True`, append the word built so far from `parts`. |

The `parts` list is a **mutable buffer** for the current path. `_dfs_words` appends
before going deeper and **pops** on the way back so siblings reuse the same list
without copying strings at every step.

Results are **sorted alphabetically** because `_dfs_words` iterates
`sorted(node.children.items())`.

---

## Walkthrough 1: `trie.collect("ca")` — prefix matches two words

This is the happy path from the unit test: both `"car"` and `"cat"` share the
prefix `"ca"`.

Expected result: **`['car', 'cat']`** (alphabetical DFS order).

### `collect("ca")` — lines 139–148

| step | line | what happens |
|------|------|--------------|
| 1 | 141 | Call `_validate_key("ca", name='prefix')`. It is a `str`, so no error. |
| 2 | 142 | Call `_find_node("ca")`. → **Find call** below |
| 3 | 143 | `node` is not `None` (the `a` node under `c`). Skip the early return. |
| 4 | 145 | `out = []` — empty result list. |
| 5 | 146 | `parts = list("ca")` → `['c', 'a']`. These characters are already consumed by navigation; DFS continues building from here. |
| 6 | 147 | Call `_dfs_words(a_node, ['c','a'], out)`. → **DFS call A** |
| 7 | 148 | Return `out` → **`['car', 'cat']`**. |

---

### Find call — `_find_node("ca")` — lines 66–74

| step | line | what happens |
|------|------|--------------|
| 1 | 68 | `_validate_key("ca", name='prefix')` — OK. |
| 2 | 69 | `node = self.root`. |
| 3 | 70–73 | Loop over `'c'`, then `'a'`: both edges exist. After `'c'` → `c_node`. After `'a'` → `a_node`. |
| 4 | 74 | Return `a_node` — the node whose children spell `"car"` and `"cat"`. |

---

### DFS call A — `_dfs_words(a_node, parts=['c','a'], out=[])`

Current node: the `a` node under `c`. It is **not** a word end (`"ca"` was never
inserted on its own). Children: `'r'` and `'t'`.

| step | line | what happens |
|------|------|--------------|
| 1 | 166 | Is `a_node.is_end`? **No** — skip append. |
| 2 | 168 | `sorted(a_node.children.items())` → `[('r', r_node), ('t', t_node)]`. Visit `'r'` first. |
| 3 | 169 | `parts.append('r')` → `['c', 'a', 'r']`. |
| 4 | 170 | Recurse → **DFS call B** on `r_node`. |
| 5 | 171 | B finished. `parts.pop()` → back to `['c', 'a']`. |
| 6 | 168 | Next sibling: `'t'`. |
| 7 | 169 | `parts.append('t')` → `['c', 'a', 't']`. |
| 8 | 170 | Recurse → **DFS call C** on `t_node`. |
| 9 | 171 | C finished. `parts.pop()` → `['c', 'a']`. |
| 10 | — | Loop done. Return to `collect()`. `out` is `['car', 'cat']`. |

---

### DFS call B — `_dfs_words(r_node, parts=['c','a','r'], out=[])`

Current node: the `r` node — marks `"car"`. Leaf (no children).

| step | line | what happens |
|------|------|--------------|
| 1 | 166 | Is `r_node.is_end`? **Yes**. |
| 2 | 167 | `out.append(''.join(['c','a','r']))` → `out = ['car']`. |
| 3 | 168 | `r_node.children` is empty — loop body never runs. Done. |

---

### DFS call C — `_dfs_words(t_node, parts=['c','a','t'], out=['car'])`

Current node: the `t` node — marks `"cat"`. Leaf.

| step | line | what happens |
|------|------|--------------|
| 1 | 166 | Is `t_node.is_end`? **Yes**. |
| 2 | 167 | `out.append(''.join(['c','a','t']))` → `out = ['car', 'cat']`. |
| 3 | 168 | No children — done. |

---

### Unwinding back to `collect()`

```text
Find    → a_node          prefix "ca" exists
DFS B   → appended "car"
DFS C   → appended "cat"
DFS A   → visited r then t in sorted order
collect → return ['car', 'cat']
```

**Takeaway:** navigation stops **at** the prefix node; DFS collects every
**complete word** in the subtree below it. The prefix itself is only included
when that node has `is_end = True` (see Walkthrough 4).

---

## Walkthrough 2: `trie.collect("coast")` — prefix path missing

`"coast"` is not stored, and the trie has no `'s'` child after the `"coa"`
segment. Navigation fails before DFS runs.

Expected result: **`[]`**.

### `collect("coast")` — lines 139–148

| step | line | what happens |
|------|------|--------------|
| 1 | 141 | `_validate_key("coast")` — OK. |
| 2 | 142 | `_find_node("coast")`. → **Find call** below |
| 3 | 143 | `node is None` → **True**. |
| 4 | 144 | **Return `[]` immediately.** `_dfs_words` is never called. |

---

### Find call — `_find_node("coast")` — lines 66–74

| step | line | what happens |
|------|------|--------------|
| 1 | 69 | `node = self.root`. |
| 2 | 70 | `ch = 'c'` — exists → move to `c_node`. |
| 3 | 70 | `ch = 'o'` — exists → move to `o_node`. |
| 4 | 70 | `ch = 'a'` — exists → move to `a_node` (under `o`). |
| 5 | 70 | `ch = 's'` — is `'s'` in `a_node.children`? **No** — only `'t'` exists. |
| 6 | 72 | **Return `None`.** |

---

### Unwinding

```text
Find    → None            "s" edge missing after "coa"
collect → return []       no DFS, trie unchanged
```

**Takeaway:** a missing character during navigation is not an error — it means
**no stored key starts with this prefix**, so the result is an empty list.

Compare with `delete("coast")`: delete also fails on a missing edge, but it
returns `False` and reports "word not found." `collect` returns `[]` because
there is nothing to list.

---

## Walkthrough 3: `trie.collect("coa")` — prefix is not a word, but a longer word exists

The path `c → o → a` exists as the start of `"coat"`, but `"coa"` itself was
never inserted. The prefix node is **not** a word end.

Expected result: **`['coat']`**.

### `collect("coa")` — lines 139–148

| step | line | what happens |
|------|------|--------------|
| 1 | 142 | `_find_node("coa")` → returns `a_node` under `o`. |
| 2 | 146 | `parts = ['c', 'o', 'a']`. |
| 3 | 147 | `_dfs_words(a_node, parts, out)`. → **DFS call A** |
| 4 | 148 | Return **`['coat']`**. |

---

### DFS call A — `_dfs_words(a_node, parts=['c','o','a'], out=[])`

Current node: the `a` node under `o`. `is_end = False`. Single child `'t'`.

| step | line | what happens |
|------|------|--------------|
| 1 | 166 | `is_end`? **No** — do not append `"coa"`. |
| 2 | 168 | Only child `'t'`. |
| 3 | 169 | `parts.append('t')` → `['c', 'o', 'a', 't']`. |
| 4 | 170 | Recurse → **DFS call B**. |
| 5 | 171 | `parts.pop()` → `['c', 'o', 'a']`. Done. |

---

### DFS call B — `_dfs_words(t_node, parts=['c','o','a','t'], out=[])`

| step | line | what happens |
|------|------|--------------|
| 1 | 166 | `t_node.is_end`? **Yes** — `"coat"` is stored. |
| 2 | 167 | `out.append('coat')` → `['coat']`. |
| 3 | 168 | Leaf — done. |

---

**Takeaway:** reaching the prefix node does **not** automatically include the
prefix string. You only append when `node.is_end` is **True** at the current
DFS position. A valid prefix of a longer word yields the longer words only.

This mirrors delete Walkthrough 3 (`delete("coa")`): the path exists, but
`is_end` at that node decides whether the prefix counts as its own key.

---

## Walkthrough 4: `trie.collect("")` — every stored word

Default argument `prefix=''` means "start DFS from the root." Every word in the
trie is a completion of the empty prefix.

Expected result: **`['car', 'cat', 'coat']`**.

### `collect("")` — lines 139–148

| step | line | what happens |
|------|------|--------------|
| 1 | 141 | `_validate_key("")` — empty string is valid. |
| 2 | 142 | `_find_node("")` — loop runs zero times → returns **`self.root`**. |
| 3 | 146 | `parts = list("")` → **`[]`**. |
| 4 | 147 | `_dfs_words(root, [], out)`. → **DFS call A** |
| 5 | 148 | Return **`['car', 'cat', 'coat']`**. |

---

### DFS call A — `_dfs_words(root, parts=[], out=[])`

| step | line | what happens |
|------|------|--------------|
| 1 | 166 | `root.is_end`? **No** (unless you inserted `""` as a key). |
| 2 | 168 | Only child `'c'`. |
| 3 | 169 | `parts.append('c')` → `['c']`. |
| 4 | 170 | Recurse → **DFS call B** on `c_node`. |
| 5 | 171 | `parts.pop()` → `[]`. Done with root. |

---

### DFS call B — `_dfs_words(c_node, parts=['c'], out=[])`

| step | line | what happens |
|------|------|--------------|
| 1 | 166 | `is_end`? **No**. |
| 2 | 168 | Sorted children: `'a'` before `'o'`. |
| 3 | 169–170 | Visit `'a'` → **DFS call C** (subtree: `"car"`, `"cat"`). |
| 4 | 171 | `parts` back to `['c']`. |
| 5 | 169–170 | Visit `'o'` → **DFS call D** (subtree: `"coat"`). |
| 6 | 171 | `parts` back to `['c']`. |

After B finishes, `out = ['car', 'cat', 'coat']`.

---

### Why `'car'` comes before `'cat'`

At the `a` node under `c`, sorted children are `'r'` then `'t'`. DFS fully
explores the `'r'` branch (yielding `"car"`) before the `'t'` branch (`"cat"`).
That is why the test asserts `['car', 'cat']`, not insertion order.

---

## Walkthrough 5: prefix that is **also** a stored word

Rebuild a smaller trie:

```python
trie = Trie()
trie.insert("ca")
trie.insert("cat")
trie.insert("car")
```

```text
root
└─ c
   └─ a *
      ├─ r *          ← "car"
      └─ t *          ← "cat"
```

`*` on `a` means `"ca"` itself is stored.

### `collect("ca")` — lines 139–148

| step | line | what happens |
|------|------|--------------|
| 1 | 142 | `_find_node("ca")` → `a_node` (which has `is_end = True`). |
| 2 | 146 | `parts = ['c', 'a']`. |
| 3 | 147 | `_dfs_words(a_node, parts, out)`. |
| 4 | 148 | Return **`['ca', 'car', 'cat']`**. |

---

### DFS call A — `_dfs_words(a_node, parts=['c','a'], out=[])`

| step | line | what happens |
|------|------|--------------|
| 1 | 166 | `a_node.is_end`? **Yes**. |
| 2 | 167 | `out.append(''.join(['c','a']))` → **`out = ['ca']`**. The prefix is a word. |
| 3 | 168 | Still visit children `'r'` and `'t'` — having `is_end = True` does not stop DFS. |
| 4 | 169–171 | Explore `'r'` → append `"car"`. Explore `'t'` → append `"cat"`. |

---

**Takeaway:** `is_end` and having children are **independent**. A node can mark
a complete word **and** continue deeper. `collect` returns the prefix **plus**
every longer word beneath it.

---

## The `parts` append / pop pattern

`_dfs_words` mutates one shared list:

```python
for ch, child in sorted(node.children.items()):
    parts.append(ch)          # extend path going down
    self._dfs_words(child, parts, out)
    parts.pop()               # undo before trying next sibling
```

Trace at the `a` node under `c` when collecting from `"ca"`:

```text
parts start:     ['c', 'a']
append 'r':      ['c', 'a', 'r']   → record "car"
pop:             ['c', 'a']
append 't':      ['c', 'a', 't']   → record "cat"
pop:             ['c', 'a']
```

Without `pop`, after visiting `"car"` the list would still end in `'r'`, and
`"cat"` would be wrongly built as `"cart"`. The pop restores the path so each
sibling starts from the same parent prefix.

Intuition: DFS on a tree uses **one stack** (here, `parts` plus the call stack).
Append on the way down, pop on the way up — classic backtracking.

---

## Cheat sheet: what each line decides

### `collect`

```python
node = self._find_node(prefix)
if node is None:
    return []
```

Prefix path broken → nothing starts with this prefix.

```python
parts: list[str] = list(prefix)
self._dfs_words(node, parts, out)
```

Seed the path buffer with characters already matched during navigation. DFS
adds only the **suffix** characters below the prefix node.

### `_find_node`

```python
for ch in prefix:
    if ch not in node.children:
        return None
    node = node.children[ch]
return node
```

Linear walk — same core loop as `search`, but **without** checking `is_end`.
Any path that exists is enough for `collect`.

### `_dfs_words`

```python
if node.is_end:
    out.append(''.join(parts))
```

Current node marks a complete stored key → record it. Checked **before**
descending so word-end nodes with children still recurse.

```python
for ch, child in sorted(node.children.items()):
```

Deterministic alphabetical order — `'car'` before `'cat'`, not insertion order.

```python
parts.append(ch)
self._dfs_words(child, parts, out)
parts.pop()
```

Go deeper with backtracking. One list, O(1) push/pop per edge instead of
copying the prefix string at every node.

---

## Quick comparison: three prefix outcomes

| call | `_find_node` | prefix node `is_end` | result |
|------|--------------|----------------------|--------|
| `collect("ca")` on cat/car/coat | found | False | `['car', 'cat']` |
| `collect("coast")` | `None` (missing `'s'`) | — | `[]` |
| `collect("coa")` on cat/car/coat | found | False | `['coat']` |
| `collect("ca")` when `"ca"` is stored | found | True | `['ca', 'car', 'cat']` |
| `collect("")` | root | usually False | all words, sorted DFS |

---

## Implementation reference

```python
def collect(self, prefix: str = '') -> list[str]:
    self._validate_key(prefix, name='prefix')
    node = self._find_node(prefix)
    if node is None:
        return []
    out: list[str] = []
    parts: list[str] = list(prefix)
    self._dfs_words(node, parts, out)
    return out

def _dfs_words(
    self,
    node: TrieNode,
    parts: list[str],
    out: list[str],
) -> None:
    if node.is_end:
        out.append(''.join(parts))
    for ch, child in sorted(node.children.items()):
        parts.append(ch)
        self._dfs_words(child, parts, out)
        parts.pop()
```
