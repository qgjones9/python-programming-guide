# Cheatcode reference

## index.md section order

1. `# [Title](https://leetcode.com/problems/{slug})` — official description
2. `## Example 1..N` + `## Constraints` — **plain**
3. `## :material-school: What you'll learn` + `!!! abstract`
4. `## Worked example data` — plain ` ```text ` block + optional example table
5. `## Approach` — brute → optimal; mermaid; walkthrough tables; admonitions at placement slots only
6. `## Implementation` — `Runnable code: [main.py](main.py)`
7. `## Solution 1: … (Best for Interview)` — 🎯 one line; complexity + Python + Java
8. `## Solution 2..N` — alternate approaches
9. `## Summary` — `__main__` block mirroring `main.py`
10. `## Industry scenarios` — emoji bullets
11. `## :material-lightbulb: Key takeaways` — emoji bullets
12. `## Internal References` — 🔗 repo links
13. `## External References` — `:fontawesome-solid-link:` URLs

## Worked example data template

```markdown
## Worked example data

Primary input for the full index-by-index trace below:

```text
# primary walkthrough input
nums = [-1, -2, -3, 0, 3, 5, -1, -2]
# expected output: 30  (subarray [3, 5, -1, -2])
```

| Example | Notes | Answer |
|---------|-------|--------|
| `[1, 2, 3, 4]` | All positive | 24 |
| `[-1, -2, -3, 0, 3, 5, -1, -2]` | Full walkthrough below | 30 |
```

**Reader-facing rules:** No lecture, transcript, ASR, professor, or video wording. Example table lists **correct** arrays only with short **Notes** (pattern labels), not transcription corrections.

## Admonition placement map

```
Constraints          → plain only
What you'll learn    → !!! abstract
Worked example data  → plain text block + optional table
Approach             → prose + tables default
                     → !!! info after recurrence / variable table
                     → !!! warning after edge cases (zero, sign flip)
                     → plain walkthrough table
                     → !!! success "Walkthrough confirmed" below table
                     → optional !!! success "30-second interview script"
Solution 1           → plain code; 🎯 in prose before heading
Key takeaways        → emoji bullets, no admonition wrapper
Industry scenarios   → emoji bullets only
```

## Emoji palette

| Emoji | Use |
|-------|-----|
| 🔑 | Pattern to memorize (Key takeaways) |
| ⚡ | Time/space win |
| 🎯 | Interview answer (before Solution 1) |
| 🧩 | Edge case |
| 💡 | Intuition (max 2 in Approach) |
| 🔗 | Internal References |
| 📊 | Optional near worked example data block |
| 📈 📡 🎮 | Industry scenarios (finance, networking, gaming) |

Material icons: `:material-school:` on What you'll learn; `:material-lightbulb:` on Key takeaways. **One anchor per heading** — emoji or Material, not both.

## Admonition syntax

```markdown
!!! warning "Interview trap: reset after zero"
    After a zero, reset running min and max to **1**, not 0. Multiplying the next
    negative by 0 kills the chain forever.
```

Body indented four spaces under the admonition line.

## 30-second interview script (optional, once per page)

```markdown
!!! success "30-second interview script"
    I scan left to right tracking the best and worst product ending at each index.
    At each step I consider the element alone and times both trackers—negatives
    flip which tracker helps. Zeros break the chain; I reset trackers to 1 and
    keep the global best seen so far.
```

## Pattern library

| Tag | Auto-consider |
|-----|----------------|
| `subarray` | [Maximum Subarray](../../docs/leetcode/blind-75/maximum-subarray/index.md); extend-or-restart `!!! info` |
| `product` | min+max DP; zero reset `!!! warning` |
| `no-division` | `!!! warning` on Product Except Self |
| `negative-numbers` | sign-flip `!!! info` |
| `zeros-in-array` | reset to 1 `!!! warning` |
| `prefix-suffix` | [Product of Array Except Self](../../docs/leetcode/blind-75/product-of-array-except-self/index.md) |

## Product subarray — edge cases (reconciliation)

| Case | Correct handling |
|------|------------------|
| Negative flip | Large `cur_min` × next negative → new `cur_max` |
| Zero | Reset `cur_min`/`cur_max` to **1**; `result = max(result, 0)` |
| Single element | `result = nums[0]` |
| All negative | min/max tracking still finds best (single element or pair) |
| Update order | Compute new min/max with **temp** vars before overwrite |

Recurrence (use temp to avoid bugs):

$$
\text{cur\_max} = \max(nums[i],\ nums[i] \times \text{cur\_max},\ nums[i] \times \text{cur\_min})
$$

$$
\text{cur\_min} = \min(nums[i],\ nums[i] \times \text{cur\_max},\ nums[i] \times \text{cur\_min})
$$

## Source sanitization (agent-only — never expose in index.md)

Remove from distilled content: welcome/intro, "let's implement", side conversations, repeated "now let's see how to solve".

Keep: variable definitions, step traces, complexity, inline arrays.

Fix silently in output: garbled numbers in transcription; wrong zero-reset (canonical: reset to **1**). Document traps in `!!! warning` without citing the source.

## Validation checklist (copy per run)

- [ ] `python3 .../main.py` passes
- [ ] LeetCode examples verified against official page
- [ ] Walkthrough array output matches trace table
- [ ] Snippet ↔ `main.py` sync
- [ ] Examples/Constraints: no admonitions/emojis
- [ ] **`index.md` has zero lecture/transcript/ASR/professor/video mentions**
- [ ] `# primary walkthrough input` in worked example block
- [ ] 3–4 admonitions for medium problems
- [ ] At least one `!!! warning` when source had a common trap
- [ ] No back-to-back admonitions
