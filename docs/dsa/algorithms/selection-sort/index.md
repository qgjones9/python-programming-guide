# Selection sort

Builds a sorted **prefix** by repeatedly choosing the next smallest (or largest) element from the unsorted suffix.

| | |
| --- | --- |
| **What it is** | For each position i, scan the rest of the array for the minimum and swap it with i. |
| **Time & space** | Θ(n²) comparisons; O(1) extra space; *not* stable as usually written. |
| **When to use** | Tiny n, or teaching (simple loop structure); rarely for large production sorts. |
| **Pattern** | “Select then place,” not insert like insertion sort. |

[Parent: Algorithms](../index.md)
