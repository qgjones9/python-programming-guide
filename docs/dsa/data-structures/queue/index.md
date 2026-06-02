# Queue

A first-in, first-out **FIFO** collection—oldest enqueued item is the next to leave.

| | |
| --- | --- |
| **What it is** | Enqueue at the rear, dequeue from the front; fair ordering of tasks or messages. |
| **Core operations** | `enqueue`, `dequeue`, often `front` / `peek`. |
| **When to use** | Job queues, BFS, buffering, and anything that should preserve arrival order. |
| **Model** | Like a line at a counter: first to arrive is first served. |

[Parent: Data structures](../index.md)
