# Quickselect

Finds the **k-th smallest** (or by rank) in expected linear time, using the same **partition** idea as quicksort.

| | |
| --- | --- |
| **What it is** | Partition; if pivot index equals k, done; else recurse only on the side that contains k. |
| **Time** | Average O(n); worst O(n²) with bad pivot choices. |
| **When to use** | Median, k-th order statistic, and quick-and-dirty selection on arrays. |
| **Related** | [Quicksort](../quicksort/index.md) recurses on both parts; this recurses on one. |

[Parent: Algorithms](../index.md)
