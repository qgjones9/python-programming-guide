# Priority queue

An abstract type: always return the item with the **highest** (or, with a custom comparator, “smallest”) priority.

| | |
| --- | --- |
| **What it is** | Not a strict “queue by time,” but a bag where *priority* orders extraction. |
| **Implementation** | Commonly a binary heap; Fibonacci heap for some graph algorithms. |
| **When to use** | Dijkstra’s algorithm, A*, task schedulers, and event simulation. |
| **Operations** | `insert`, `extract_best`, sometimes `decrease_priority`. |

[Parent: Data structures](../index.md)
