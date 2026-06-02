# Bubble sort

Pass through the array, **swapping adjacent** out-of-order pairs; repeat until a pass does nothing.

| | |
| --- | --- |
| **What it is** | After each pass, the largest element “bubbles” to its end. |
| **Time & space** | Θ(n²) comparisons; O(1) space; with a flag, can finish early on already sorted. |
| **When to use** | Teaching and tiny n; almost never the right choice in production. |
| **Stability** | Stable if you only swap on strict `<`. |

[Parent: Algorithms](../index.md)
