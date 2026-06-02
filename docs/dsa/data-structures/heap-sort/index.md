# Heap sort

A **comparison sort** that uses a max-heap: repeatedly pull the maximum to the end and repair the heap.

| | |
| --- | --- |
| **What it is** | Build a heap in O(n), then n−1 times extract-max and place at the end of the array. |
| **Time** | O(n log n) worst case, O(1) extra space (in place on the array). |
| **Property** | Not stable (equal items may change relative order) unless you adapt carefully. |
| **When to use** | You want in-place, predictable O(n log n) and already understand heaps. |

[Parent: Data structures](../index.md)
