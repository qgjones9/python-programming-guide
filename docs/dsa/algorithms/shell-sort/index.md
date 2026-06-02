# Shell sort

A **gap-based** variant of insertion sort: sort elements *g* apart, then reduce *g* until 1 (plain insertion sort).

| | |
| --- | --- |
| **What it is** | Generalizes insertion sort by moving elements long distances early, then tightening the gap. |
| **Time** | Depends on gap sequence; better than O(n²) for some sequences, still not O(n log n) in worst case for naive choices. |
| **Space** | O(1) in place. |
| **When to use** | Embedded or legacy code paths; conceptually between insertion and fast O(n log n) sorts. |

[Parent: Algorithms](../index.md)
