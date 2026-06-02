# Merge sort

**Split** the array in half, sort each half **recursively**, then **merge** the two sorted halves in linear time.

| | |
| --- | --- |
| **What it is** | Merge combines two sorted ranges by two pointers; main work is in the merge step. |
| **Time & space** | O(n log n) worst case; needs O(n) extra space for a typical array merge. |
| **When to use** | Stable sort required, linked lists, external sort, or parallel merge sort. |
| **Stability** | Keep left equal elements before right when merging. |

[Parent: Algorithms](../index.md)
