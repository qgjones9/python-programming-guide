# Number of Islands

## Review links

Start with **2D grids** and **Graphs** (BFS/DFS + connected components). Number of Islands is a grid **flood-fill** / **connected-component** count.

### Essential (read these first)

| Topic | Why it matters for this problem | Link |
| --- | --- | --- |
| 2D grids | Flood fill, in-place `'1'` → `'0'` marking, `count_components` DFS template | [2D grids](../../../dsa/data-structures/2d-grids/index.md) |
| Graphs — implicit grids | Each cell is a vertex; 4-direction neighbors; O(R × C) traversal | [Graphs — implicit grids](../../../dsa/data-structures/graphs/index.md#implicit-graphs-grids) |
| Graphs — DFS | Depth-first flood fill (sink the island) | [Graphs — DFS](../../../dsa/data-structures/graphs/index.md#dfs--depth-first-search) |
| Graphs — BFS | Queue-based flood fill alternative | [Graphs — BFS](../../../dsa/data-structures/graphs/index.md#bfs--breadth-first-search) |
| Graphs — connected components | Same idea as counting islands on an adjacency-list graph | [Graphs — `connected_components`](../../../dsa/data-structures/graphs/index.md#connected_components--isolated-road-regions) |
| Graph theory — connected component | Vocabulary: maximal reachable set of vertices | [Graph theory — connected component](../../../dsa/data-structures/graphs/graph-theory/index.md#connected-component) |

### Supporting references

| Topic | Why it matters for this problem | Link |
| --- | --- | --- |
| Recursion | Recursive DFS on grid neighbors | [Recursion](../../../dsa/recursion/index.md) |
| Deque | `collections.deque` for BFS (`popleft` in O(1)) | [Dequeue (deque)](../../../dsa/data-structures/dequeue-deque/index.md) |
| Queue | FIFO mental model behind BFS | [Queue](../../../dsa/data-structures/queue/index.md) |
| Union-Find | Alternate O(R × C) approach without flood fill | [Honorable mention ADT — Union-Find](../../../dsa/data-structures/honorable-mention-adt/index.md#union-find-disjoint-set) |
| Backtracking | Grid DFS with visit/undo (Word Search pattern) | [Backtracking](../../../dsa/algorithms/backtracking/index.md) |
| Complexity | O(R × C) time and space notation | [Complexity analysis](../../../dsa/complexity/index.md) |
| Data structures hub | Index of all structure pages | [Data structures](../../../dsa/data-structures/index.md) |
| Graphs hub (full page) | Representations, traversals, algorithm picker | [Graphs](../../../dsa/data-structures/graphs/index.md) |

### This problem (solution write-up)

| Topic | Link |
| --- | --- |
| Number of Islands — study guide + code | [index.md](./index.md) |
