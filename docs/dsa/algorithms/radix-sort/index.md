# Radix sort

Sorts by **processing digits (or character positions) from least to most** significant, using a stable pass each time.

| | |
| --- | --- |
| **What it is** | Not a pure comparison sort: uses counting/bucket on each digit place. |
| **Time** | O(d · (n + k)) for n keys, d digits, alphabet size k per digit. |
| **When to use** | Fixed-width integers, strings of equal length, or when digits are small. |
| **Requirement** | Stable sub-sorts; keys must be splittable into digits/buckets meaningfully. |

[Parent: Algorithms](../index.md)
