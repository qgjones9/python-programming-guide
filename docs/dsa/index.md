# Data structures and algorithms

| Section | Topic | Highlights |
|---|---|---|
| :material-chart-timeline-variant: [Complexity analysis](complexity/index.md) | Foundations | Big-O, time and space, best / average / worst case, amortized cost |
| :material-source-branch: [Recursion](recursion/index.md) | Foundations | Base cases, call stack, divide-and-conquer, trees and graph DFS |
| :material-graph: [Data Structures](data-structures/index.md) | Data structures | Arrays, linked lists, trees, graphs, 2D grids, hash tables, heaps, queues, stacks |
| :material-sort-variant: [Algorithms](algorithms/index.md) | Algorithms | Sorting, searching, backtracking, dynamic programming, graph algorithms, greedy methods |


## Learning roadmap

Work through the phases below in order. Each phase assumes the previous one; jump ahead only when you already know that material. Use the [data structures](data-structures/index.md) and [algorithms](algorithms/index.md) hubs for full page lists.

### Phase 0 — Foundations

Before diving into implementations, be comfortable with:

| # | Topic | Description |
|---|-----------|-------------|
| 1 | [Complexity analysis](complexity/index.md) | Big-O time and space; best, average, and worst case; how to read cost rows on other pages. |
| 2 | [Recursion](recursion/index.md) | Base cases, call stack intuition, and when recursion maps naturally to trees and divide-and-conquer. |
| 3 | [Python tutorial](../versions/3.14.5/tutorial/index.md) | Lists, dicts, sets, and loops; you will reimplement many of these ideas by hand in the DSA pages. |


### Phase 1 — Linear structures

Start with structures that model a sequence and support predictable access patterns:

| # | Structure | Description |
|---|-----------|-------------|
| 1 | [Array-based lists](data-structures/array-based-lists/index.md) | Contiguous storage, indexing, amortized growth. |
| 2 | [Linked list](data-structures/linked-list/index.md) → [Doubly linked list](data-structures/doubly-linked-list/index.md) → [Circularly linked list](data-structures/circularly-linked-list/index.md) | Pointer chasing, O(1) head insert, no random access. |
| 3 | [Stacks](data-structures/stacks/index.md) and [Queue](data-structures/queue/index.md) | LIFO and FIFO; building blocks for parsers and BFS. |
| 4 | [Deque](data-structures/dequeue-deque/index.md) | O(1) operations at both ends. |
| 5 | [2D grids](data-structures/2d-grids/index.md) | Nested lists, indexing, spiral/rotate traversal; foundation for grid search. |

### Phase 2 — Hashing and fast lookup

When you need average O(1) lookup by key:

| # | Structure | Description |
|---|-----------|-------------|
| 1 | [Hash table](data-structures/hash-table/index.md) | Hash functions, handle collisions, manage load factor. |
| 2 | [Set](data-structures/sets/index.md) | Enforce uniqueness and quick membership checks using hashes or trees. |

### Phase 3 — Trees and priority

Ordered and hierarchical data:

| # | Structure | Description |
|---|-----------|-------------|
| 1 | [Binary search tree](data-structures/binary-search-tree/index.md) | Ordering invariant, search, insert, delete. |
| 2 | [AVL tree](data-structures/avl-tree/index.md) | Self-balancing BST, rotations keep height O(log n). |
| 3 | [Red–black tree](data-structures/red-black-tree/index.md) | Self-balancing BST with a coloring rule; used in many library maps/sets. |
| 4 | [2-3-4 tree](data-structures/2-3-4-tree/index.md) | Self-balancing search tree; nodes with 2, 3, or 4 children (B-tree family). |

### Phase 4 — Graphs

Model relationships, dependencies, and networks:

| # | Topic | Description |
| --- | --- | --- |
| 1 | [Graphs](data-structures/graphs/index.md) | Representations (adjacency list vs matrix), directed vs undirected, BFS, DFS, topological sort; use the hub **algorithm picker** for weighted paths and MSTs. |
| 2 | [Dijkstra](data-structures/graphs/dijkstra/index.md) | Single-source shortest paths when edge weights are non-negative. |
| 3 | [Bellman–Ford](data-structures/graphs/bellman-ford/index.md) | Single-source shortest paths with negative weights; detect negative cycles. |
| 4 | [Floyd–Warshall](data-structures/graphs/floyd-warshall/index.md) | All-pairs shortest paths (optional after single-source algorithms). |
| 5 | [A*](data-structures/graphs/a-star/index.md) | Heuristic search when you have a goal and admissible estimate (optional). |
| 6 | [Minimum spanning tree](data-structures/graphs/minimum-spanning-tree/index.md) | Kruskal and Prim for connected undirected weighted networks. |
| 7 | [2D grids](data-structures/2d-grids/index.md) | When the graph is a board: neighbor loops, BFS/DFS templates, implicit vertices at each cell. |

### Phase 5 — Core algorithms

With structures in place, study classic algorithms and their tradeoffs:

**Sorting** (comparison-based first, then distribution-based):

| Order | Topic | Page |
| --- | --- | --- |
| 1 | Bubble, selection, insertion | [Bubble sort](algorithms/bubble-sort/index.md), [selection sort](algorithms/selection-sort/index.md), [insertion sort](algorithms/insertion-sort/index.md) |
| 2 | Shell sort | [Shell sort](algorithms/shell-sort/index.md) |
| 3 | Merge sort, quicksort | [Merge sort](algorithms/merge-sort/index.md), [Quicksort](algorithms/quicksort/index.md) |
| 4 | Radix, bucket | [Radix sort](algorithms/radix-sort/index.md), [Bucket sort](algorithms/bucket-sort/index.md) |

**Searching and selection** — binary search on sorted arrays; [quickselect](algorithms/quickselect/index.md) for order statistics.

**Beyond sorting** — [backtracking](algorithms/backtracking/index.md), [dynamic programming](algorithms/dynamic-programming/index.md), graph algorithms (flows, MSTs), and greedy methods. Tackle these after Phases 1–4 when you can write recurrences and trace choose/undo search.

### Phase 6 — Practice and integration

Tie structures and algorithms together:

- **Implement, then compare** — code a structure or algorithm from scratch, then contrast with `list`, `dict`, `collections.deque`, `heapq`, and `bisect`.
- **Pick the right tool** — e.g. BFS + queue for unweighted shortest paths; Dijkstra + priority queue for non-negative weights; hash table for frequency counts; trie for prefix queries.
- **Pattern recognition** — two pointers, sliding window, divide and conquer, and memoization often reuse the same building blocks from Phases 1–5.
- **Deliberate practice** — solve varied problems (easy → medium), analyze your solution’s time and space, and refactor when a better structure applies.

See also [honorable mention ADT](data-structures/honorable-mention-adt/index.md) for adjacent abstract data types worth knowing after the core path.