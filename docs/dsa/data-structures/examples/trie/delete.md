# Trie delete walkthrough

This README traces `delete()` line by line so you can see exactly what the
code does. Start with a trie that already stores **cat** and **coat**.

## Starting trie

After:

```python
trie = Trie()
trie.insert("cat")
trie.insert("coat")
```

`len(trie)` is **2**. The tree looks like this (`*` = word end):

```text
root
└─ c
   ├─ a
   │  └─ t *          ← "cat"
   └─ o
      └─ a
         └─ t *       ← "coat"
```

Shared idea: `_delete_from(node, word, depth)` walks one character at a time.
It always returns a pair:

| return value   | meaning |
|----------------|---------|
| `removed`      | Did we actually unmark a stored word? |
| `should_prune` | Should the **parent** remove its link to this node because it's no longer needed? |

---

## Walkthrough 1: `trie.delete("coast")` — word not in trie

`"coast"` is **not** stored. The path `c → o → a` exists (prefix of `"coat"`), but
there is no `s` child after `a`. The delete fails without changing the trie.

### `delete("coast")` — lines 123–137

| step | line | what happens |
|------|------|--------------|
| 1 | 132 | Call `_validate_key("coast")`. It is a `str`, so no error. |
| 2 | 133 | Call `_delete_from(self.root, "coast", 0)`. |
| 3 | 134 | `removed` is `False`, so skip the `if removed` block. |
| 4 | 137 | Return `False`. Trie still has `"cat"` and `"coat"`; `_size` stays `2`. |

---

### Call A — `_delete_from(root, "coast", depth=0)`

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | Is `depth == len("coast")`? `0 == 5` → **No**. Not at the end of the word yet. |
| 2 | 114 | `ch = word[0]` → `ch = 'c'`. |
| 3 | 115 | Is `'c'` in `root.children`? **Yes** (inserted by both words). |
| 4 | 117 | `child = root.children['c']` → the `c` node. |
| 5 | 118 | Recurse: `_delete_from(c_node, "coast", 1)`. → **Call B** |
| 6 | 119 | B returned `should_prune = False`, so skip `del`. |
| 7 | 121 | Return `(False, False)` because `c_node` still has children and is not a word end. |

---

### Call B — `_delete_from(c_node, "coast", depth=1)`

Current node: the `c` node (children: `'a'`, `'o'`).

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `1 == 5`? **No**. |
| 2 | 114 | `ch = word[1]` → `ch = 'o'`. |
| 3 | 115 | Is `'o'` in `c_node.children`? **Yes** (`"coat"` path). |
| 4 | 117 | `child = c_node.children['o']` → the `o` node. |
| 5 | 118 | Recurse: `_delete_from(o_node, "coast", 2)`. → **Call C** |
| 6 | 119 | C returned `should_prune = False`, so skip `del`. |
| 7 | 121 | Return `(False, False)` — `o_node` still has child `'a'`. |

---

### Call C — `_delete_from(o_node, "coast", depth=2)`

Current node: the `o` node (child: `'a'`).

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `2 == 5`? **No**. |
| 2 | 114 | `ch = word[2]` → `ch = 'a'`. |
| 3 | 115 | Is `'a'` in `o_node.children`? **Yes**. |
| 4 | 117 | `child = o_node.children['a']` → the `a` node under `o`. |
| 5 | 118 | Recurse: `_delete_from(a_node, "coast", 3)`. → **Call D** |
| 6 | 119 | D returned `should_prune = False`, so skip `del`. |
| 7 | 121 | Return `(False, False)`. |

---

### Call D — `_delete_from(a_node, "coast", depth=3)` ← failure happens here

Current node: the `a` node under `o` (child: `'t'` only — that edge spells `"coat"`, not `"coast"`).

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `3 == 5`? **No**. |
| 2 | 114 | `ch = word[3]` → `ch = 's'`. |
| 3 | 115 | Is `'s'` in `a_node.children`? **No** — only `'t'` exists. |
| 4 | 116 | **Return `(False, False)` immediately.** No nodes are modified. No pruning. |

---

### Unwinding back to `delete()`

```text
Call D  → (False, False)   "s" missing — stop here
Call C  → (False, False)   nothing to prune
Call B  → (False, False)   nothing to prune
Call A  → (False, False)   nothing to prune
delete  → return False     _size unchanged
```

**Takeaway:** when the next character is missing, the recursion bails out early
with `(False, False)`. The trie is untouched.

---

## Walkthrough 2: `trie.delete("coat")` — word found and pruned

Same starting trie. This time the word **is** stored. This shows the
`depth == len(word)` branch and branch pruning your example described.

### `delete("coat")` — lines 123–137

| step | line | what happens |
|------|------|--------------|
| 1 | 132 | `_validate_key("coat")` — OK, it is a `str`. |
| 2 | 133 | `_delete_from(self.root, "coat", 0)`. |
| 3 | 134 | `removed` is `True`. |
| 4 | 135 | `self._size -= 1` → `_size` goes from `2` to `1`. |
| 5 | 136 | Return `True`. |

---

### Call A — `_delete_from(root, "coat", depth=0)`

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `0 == 4`? **No**. |
| 2 | 114 | `ch = 'c'`. |
| 3 | 115–117 | `'c'` exists → follow to `c_node`. |
| 4 | 118 | Recurse → **Call B**. |
| 5 | 119 | B returns `should_prune = False` (`c_node` still has `'a'` for `"cat"`). |
| 6 | 121 | Return `(True, False)`. |

---

### Call B — `_delete_from(c_node, "coat", depth=1)`

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `1 == 4`? **No**. |
| 2 | 114 | `ch = 'o'`. |
| 3 | 115–117 | `'o'` exists → follow to `o_node`. |
| 4 | 118 | Recurse → **Call C**. |
| 5 | 119 | C returns `should_prune = True` → **`del c_node.children['o']`**. The entire `o → a → t` branch is removed from the `c` node. |
| 6 | 121 | Return `(True, False)` — `c_node` still has child `'a'` (`"cat"`), so do not prune `c` itself. |

---

### Call C — `_delete_from(o_node, "coat", depth=2)`

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `2 == 4`? **No**. |
| 2 | 114 | `ch = 'a'`. |
| 3 | 115–117 | `'a'` exists → follow to `a_node`. |
| 4 | 118 | Recurse → **Call D**. |
| 5 | 119 | D returns `should_prune = True` → **`del o_node.children['a']`**. |
| 6 | 121 | Return `(True, True)` — `o_node` is now empty and not a word end → parent should remove `o`. |

---

### Call D — `_delete_from(a_node, "coat", depth=3)`

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `3 == 4`? **No**. |
| 2 | 114 | `ch = 't'`. |
| 3 | 115–117 | `'t'` exists → follow to `t_node`. |
| 4 | 118 | Recurse → **Call E**. |
| 5 | 119 | E returns `should_prune = True` → **`del a_node.children['t']`**. |
| 6 | 121 | Return `(True, True)` — `a_node` is empty → parent should remove `a`. |

---

### Call E — `_delete_from(t_node, "coat", depth=4)` ← word end reached

Current node: the `t` node that marks `"coat"`. It is a leaf (no children).

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `4 == 4`? **Yes** — consumed all characters of `"coat"`. |
| 2 | 109 | Is `t_node.is_end`? **Yes** — this node stores a complete word. |
| 3 | 111 | `t_node.is_end = False` — unmark `"coat"` (node still exists for now). |
| 4 | 112 | `t_node.value = None` — clear any payload. |
| 5 | 113 | Return `(True, len(t_node.children) == 0)` → **`(True, True)`** — leaf with no children, safe to prune. |

If step 2 had been **No** (`is_end` is `False`), line 110 would return
`(False, False)` — see **Walkthrough 3** (`delete("coa")`) for that case.

---

### Final trie after `delete("coat")`

```text
root
└─ c
   └─ a
      └─ t *          ← only "cat" remains
```

---

## Walkthrough 3: `trie.delete("coa")` — path exists, but not a stored word

Same starting trie (`"cat"`, `"coat"`). `"coa"` is a **prefix** of `"coat"`, not a
word stored on its own. The walk reaches the node at the end of `"coa"`, but that
node has `is_end = False` because only the deeper `"t"` node marks `"coat"`.

This is the third failure mode:

| failure mode | where it fails | line |
|--------------|----------------|------|
| missing edge | mid-path (`"coast"`) | 115–116 |
| path exists, not a word | at last character (`"coa"`) | 109–110 |
| word found | at last character (`"coat"`) | 111–113 |

### `delete("coa")` — lines 123–137

| step | line | what happens |
|------|------|--------------|
| 1 | 132 | `_validate_key("coa")` — OK, it is a `str`. |
| 2 | 133 | `_delete_from(self.root, "coa", 0)`. |
| 3 | 134 | `removed` is `False`, so skip the `if removed` block. |
| 4 | 137 | Return `False`. Trie unchanged; `_size` stays `2`. |

---

### Call A — `_delete_from(root, "coa", depth=0)`

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `0 == 3`? **No**. |
| 2 | 114 | `ch = 'c'`. |
| 3 | 115–117 | `'c'` exists → follow to `c_node`. |
| 4 | 118 | Recurse → **Call B**. |
| 5 | 119 | B returns `should_prune = False`, so skip `del`. |
| 6 | 121 | Return `(False, False)`. |

---

### Call B — `_delete_from(c_node, "coa", depth=1)`

Current node: the `c` node (children: `'a'`, `'o'`).

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `1 == 3`? **No**. |
| 2 | 114 | `ch = 'o'`. |
| 3 | 115–117 | `'o'` exists → follow to `o_node`. |
| 4 | 118 | Recurse → **Call C**. |
| 5 | 119 | C returns `should_prune = False`, so skip `del`. |
| 6 | 121 | Return `(False, False)`. |

---

### Call C — `_delete_from(o_node, "coa", depth=2)`

Current node: the `o` node (child: `'a'`).

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `2 == 3`? **No**. |
| 2 | 114 | `ch = 'a'`. |
| 3 | 115–117 | `'a'` exists → follow to `a_node` (under `o`). |
| 4 | 118 | Recurse → **Call D**. |
| 5 | 119 | D returns `should_prune = False`, so skip `del`. |
| 6 | 121 | Return `(False, False)` — `a_node` still has child `'t'`. |

---

### Call D — `_delete_from(a_node, "coa", depth=3)` ← failure happens here

Current node: the `a` node under `o`. It is **not** a word end (`is_end = False`);
only its `'t'` child completes `"coat"`. It still has one child.

| step | line | what happens |
|------|------|--------------|
| 1 | 108 | `3 == 3`? **Yes** — consumed all characters of `"coa"`. |
| 2 | 109 | Is `a_node.is_end`? **No** — `"coa"` was never inserted as its own key. |
| 3 | 110 | **Return `(False, False)` immediately.** No fields changed. No pruning. |

Compare with Walkthrough 2 Call E: same `depth == len(word)` check, but there
`is_end` was **True** so lines 111–113 ran instead.

---

### Unwinding back to `delete()`

```text
Call D  → (False, False)   path exists but is_end is False — stop here
Call C  → (False, False)   nothing to prune (a_node still has child "t")
Call B  → (False, False)   nothing to prune
Call A  → (False, False)   nothing to prune
delete  → return False     _size unchanged
```

**Takeaway:** reaching the last character does **not** mean the delete succeeds.
The node must also be marked `is_end = True`. A prefix-only path like `"coa"`
looks valid while walking down, then fails at the base case.

Trie after `delete("coa")` — identical to the start:

```text
root
└─ c
   ├─ a
   │  └─ t *          ← "cat"
   └─ o
      └─ a
         └─ t *       ← "coat"
```

---

## Cheat sheet: what each line in `_delete_from` decides

```python
if depth == len(word):
```

We have walked every character. Either unmark the word (if stored) or report
"not found".

```python
if not node.is_end:
    return False, False
```

The path exists but nobody stored a word ending **here** (e.g. deleting
`"coa"` when only `"coat"` is stored).

```python
node.is_end = False
node.value = None
return True, len(node.children) == 0
```

Word removed. Tell parent to delete this node only if it has **no** leftover
children (otherwise other words still use this prefix).

```python
ch = word[depth]
if ch not in node.children:
    return False, False
```

Next character missing — word was never stored down this path (`"coast"` case).

```python
removed, should_prune = self._delete_from(child, word, depth + 1)
if should_prune:
    del node.children[ch]
return removed, len(node.children) == 0 and not node.is_end
```

Go deeper. If the child became useless, cut the edge. Then tell **our** parent
whether **we** became useless (no children left and we are not a word end).
