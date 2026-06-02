# Quicksort

**Partition** the array around a pivot so left ≤ pivot ≤ right, then recurse on each side—classic divide and conquer.

| | |
| --- | --- |
| **What it is** | Choose a pivot, rearrange so smaller left, larger right, then quicksort each part. |
| **Time & space** | Average O(n log n), worst O(n²) with bad pivots; O(log n) stack typically, in place. |
| **When to use** | General in-memory sorts; random or three-median pivot reduces bad cases. |
| **Not stable** | Standard in-place partition swaps break stable order. |

[Parent: Algorithms](../index.md)
