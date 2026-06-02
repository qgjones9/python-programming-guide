# Max heap

A **complete** binary tree where each parent’s key is **≥** all keys in its subtrees (max-heap property).

| | |
| --- | --- |
| **What it is** | Usually stored in an array: parent/child index formulas avoid explicit child pointers. |
| **Core operations** | `insert`, `extract_max`, sometimes `increase_key`—all in O(log n) height. |
| **When to use** | Priority scheduling, k largest elements, and as the building block of heap sort. |
| **Min-heap** | The same idea with parent ≤ children. |

[Parent: Data structures](../index.md)
