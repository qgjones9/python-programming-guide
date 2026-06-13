---
name: cheatcode
description: >-
  Turns LeetCode lecture/transcript files into interview-ready blind-75 notes
  (index.md) and runnable solutions (main.py). Distills ASR lectures into tutor-voice
  study guides with selective admonitions and emojis on traps and confirmations.
  Use when the user invokes cheatcode, asks for LeetCode solution notes from a
  lecture, or says "same here" for docs/leetcode/blind-75 with transcript.md or
  lecture.md.
---

# Cheatcode — LeetCode Solution Notes

## Goal

Transform a raw lecture file into a **single study reference**: [`index.md`](../../docs/leetcode/blind-75/) + [`main.py`](../../docs/leetcode/blind-75/) in the problem folder. Do **not** edit the lecture/transcript source file.

**Not** for interim formatting — do not use [`format-lecture-notes`](~/.cursor/skills/format-lecture-notes/SKILL.md) for final blind-75 pages. Distill; never paste verbatim ASR quirks.

## Inputs

| Input | Resolution |
|-------|------------|
| Lecture | `lecture.md` → else `transcript.md` → else `transcript.txt` |
| Problem folder | User `@` path or parent of lecture file |
| Slug | Folder name (e.g. `maximum-product-subarray`) |
| Reference sibling | Latest completed page in same pattern family; default [`maximum-subarray/index.md`](../../docs/leetcode/blind-75/maximum-subarray/index.md) or [`two-sum/index.md`](../../docs/leetcode/blind-75/two-sum/index.md) |
| LeetCode URL | `https://leetcode.com/problems/{slug}/` — fetch statement, examples, constraints; **verify** against running code |

Parse optional ` ```text ` blocks tagged `# collection of data used in the problem statement`.

## Workflow

1. Read lecture + current stub `index.md`
2. Read reference sibling for section naming, tables, Solution order (optimal first), Java block
3. Sanitize lecture: drop meta, side conversations, filler; keep algorithm claims, variables, traces, complexity; fix array typos (`3-4` → `3, -4`)
4. Reconcile lecture vs canonical algorithm; fix ASR errors (document corrections in `!!! warning` when lecture was wrong)
5. Write `index.md` + `main.py` in parallel (matching function names/signatures)
6. Run validation (below)
7. Add Internal/External References

See [reference.md](reference.md) for full `index.md` template, emoji palette, pattern library, and edge-case table.

## Voice

- Second person tutor: "You track…", "Let's break this down…"
- Never: "The professor says…", "In this video…", "According to the transcript…"
- Tables for 3+ parallel facts ([markdown-tables rule](../../.cursor/rules/markdown-tables-over-long-lists.mdc))

## Hybrid format

Preserve the **interview skeleton** from completed blind-75 pages:

`LeetCode I/O → Approach (brute → optimal) → walkthrough tables → Solution 1..N → Summary`

Insert enrichment **around** that core: What you'll learn, Lecture walkthrough data, Implementation link, Industry scenarios, Key takeaways, References.

Keep `## Approach` and `## Solution 1` headings **plain** (no Material icons).

## Selective emphasis (admonitions + emojis)

Admonitions/emojis are **highlighters**, not decoration. Before each admonition, answer **yes** to at least one:

- Would a candidate get this wrong in an interview without the callout?
- Did the lecture say something incorrect?
- Is this the one sentence you'd skim before a phone screen?
- Does this confirm input → output after a long trace?

If all no → plain prose or table.

### Admonition types (four only)

| Type | When |
|------|------|
| `!!! abstract` | Once in **What you'll learn** |
| `!!! info` | Recurrence, variable roles, non-obvious intuition |
| `!!! warning` | Interview traps; lecture vs canonical fix |
| `!!! success` | Confirmed walkthrough result; optional 30-second interview script (max once) |

**Keep plain:** Examples, Constraints, complexity tables, walkthrough tables, code fences.

**Hard stops:** No back-to-back admonitions; no emojis on table rows or code; Examples/Constraints have zero admonitions/emojis; indent admonition bodies **4 spaces**.

### Density

| Difficulty | Admonitions |
|------------|-------------|
| Easy | 2 (`abstract` + one `info` or `warning`) |
| Medium + edge cases | 3–4 |
| Hard | up to 5 |

Emojis on **Key takeaways**, **Industry scenarios**, at most 2 intuition bullets in Approach, 🎯 before Solution 1.

Full placement map and emoji palette: [reference.md](reference.md).

## main.py conventions

Match [`maximum-subarray/main.py`](../../docs/leetcode/blind-75/maximum-subarray/main.py):

- Module docstring: problem, example I/O, `Author: python-programming-guide`
- One function per approach; docstring includes Time/Space complexity
- `if __name__ == "__main__":` prints all approaches; include lecture array when present

Sync primary Python snippet in `index.md` with `main.py` bodies.

## Validation

```bash
python3 docs/leetcode/blind-75/{slug}/main.py
```

Plus `python3 -c` import assertions for LeetCode examples and edge cases (single element, zeros, all negative).

Checklist:

- [ ] LeetCode examples match official page and running code
- [ ] Primary snippet matches `main.py`
- [ ] Lecture file untouched
- [ ] `[main.py](main.py)` link in `## Implementation`
- [ ] Admonition count matches density table
- [ ] At least one `!!! warning` if lecture contradicted canonical solution
- [ ] Mermaid flowchart for non-trivial control flow
- [ ] Internal links to related blind-75 siblings

## Pattern tags (scan lecture + problem)

| Tag | Action |
|-----|--------|
| `subarray` | Link Maximum Subarray; Kadane `!!! info` |
| `product` | min+max tracker; zero reset `!!! warning` |
| `no-division` | `!!! warning` |
| `negative-numbers` | sign-flip `!!! info` |
| `zeros-in-array` | reset semantics `!!! warning` |

## Do not

- Edit the plan file or lecture source
- Use `format-lecture-notes` for final `index.md`
- Wrap entire Approach subsections in admonitions
- Add nav/mkdocs changes unless user asks
