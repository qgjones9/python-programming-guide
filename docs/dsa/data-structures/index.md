# Data structures

This hub lists every data-structure page in this section. Each page opens with a short table describing what the structure is, how it behaves, and when it helps.

| Topic | What it is | Page |
| --- | --- | --- |
| Linked list | A chain of nodes (value + next pointer). Good for head inserts; no O(1) index access. | [Linked list](linked-list/index.md) |
| Doubly linked list | Like a linked list, but each node also points to the previous node. | [Doubly linked list](doubly-linked-list/index.md) |
| Circularly linked list | Last node’s next points to the first—forms a ring; handy for round-robin iteration. | [Circularly linked list](circularly-linked-list/index.md) |
| Array-based lists | A list backed by a contiguous array (fixed or resizable, e.g. `vector` / `ArrayList`). | [Array-based lists](array-based-lists/index.md) |
| Stacks | LIFO structure: `push` / `pop` (and usually `peek`). | [Stacks](stacks/index.md) |
| Queue | FIFO structure: `enqueue` at one end, `dequeue` at the other. | [Queue](queue/index.md) |
| Dequeue (deque) | Double-ended queue: O(1) add/remove at both ends. | [Dequeue (deque)](dequeue-deque/index.md) |
| Hash table | Maps keys to values using a hash function and a collision policy; average O(1) operations. | [Hash table](hash-table/index.md) |
| Tries | Tree keyed by string prefixes; fast prefix search and auto-complete style queries. | [Tries](tries/index.md) |
| Binary search tree | Binary tree with ordering: left < node < right; enables ordered search. | [Binary search tree](binary-search-tree/index.md) |
| AVL tree | Self-balancing BST: rotations keep height O(log n). | [AVL tree](avl-tree/index.md) |
| Red–black tree | Self-balancing BST with a coloring rule; used in many library maps/sets. | [Red–black tree](red-black-tree/index.md) |
| Max heap | Complete binary tree where each parent is ≥ its children; supports fast max extract. | [Max heap](max-heap/index.md) |
| Min heap | Complete binary tree where each parent is ≤ its children; supports fast min extract. | [Min heap](min-heap/index.md) |
| Priority queue | ADT: always return the element with the highest (or custom) priority. | [Priority queue](priority-queue/index.md) |
| Heap sort | In-place sort: build a heap, then repeatedly take the extrema. | [Heap sort](heap-sort/index.md) |
| Treaps | BST where nodes carry random heap priority—simple randomized balance. | [Treaps](treaps/index.md) |
| Sets | Collection of unique elements, usually via hash or tree behind the scenes. | [Sets](sets/index.md) |
| Graphs | Vertices and edges; used for networks, dependencies, and paths. | [Graphs](graphs/index.md) |
| 2-3-4 tree | Self-balancing search tree; nodes with 2, 3, or 4 children (B-tree family). | [2-3-4 tree](2-3-4-tree/index.md) |
| Honorable mention ADT | Other classic ADTs worth a nod when they do not have their own page here. | [Honorable mention ADT](honorable-mention-adt/index.md) |

Back to the [DSA overview](../index.md).
