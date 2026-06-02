# Treaps

A **tree + heap** hybrid: a BST by key, and each node has a **random** priority to keep shape balanced in expectation.

| | |
| --- | --- |
| **What it is** | Keys obey BST order; random priorities obey heap order (e.g. parent priority ≥ children’s). |
| **Why it works** | Random priorities mimic the shape of a random binary search tree on average. |
| **When to use** | Simpler to implement than red–black for some, mergeable with split/join. |
| **Expectation** | O(log n) height with high probability. |

[Parent: Data structures](../index.md)
