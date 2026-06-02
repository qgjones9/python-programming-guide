# Graphs

A **graph** is a set of **vertices** (nodes) and **edges** (links). Edges may be **directed** or **undirected**, **weighted** or **unweighted**. Graphs model **relationships**, **dependencies**, **routes**, and **state machines**—not just “maps.”

| | |
| --- | --- |
| **What it is** | G = (V, E); vertices are entities, edges are connections with optional weight. |
| **Representations** | Adjacency list (sparse), adjacency matrix (dense), edge list (compact storage). |
| **Core algorithms** | BFS, DFS, topological sort, shortest paths, minimum spanning tree, connected components. |
| **When to use** | Team networks, schedule graphs, play-drive state machines, coaching trees, travel between cities. |

In **NFL data analysis**, graphs appear as **team relationship networks** (who played whom), **division connectivity**, **coach reporting lines**, and **drive state transitions** (down/distance nodes). You will still aggregate stats in **pandas**—graphs excel when the question is **reachability**, **shortest path**, or **connectivity**.

This page is your **ready reference**: representations, a complete Python adjacency-list implementation, traversals with Mermaid, every common operation with NFL examples, and **time and space complexity**. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## How graphs fit NFL-shaped problems

| NFL idea | Graph model | Typical algorithm |
| --- | --- | --- |
| **Season schedule** | Vertices = teams; edge = game played | Degree count, neighbor lists |
| **Coach hierarchy** | Directed tree | DFS, topological order |
| **Travel: KC → BUF** | Weighted cities | Dijkstra / A* |
| **Play similarity chain** | Directed edges “next likely play” | BFS layers |
| **Conference connectivity** | Undirected teams in same conference component | Union-Find / DFS |
| **Rivalry pairs** | Undirected unweighted | Set of edges |

```mermaid
flowchart LR
  KC["KC"] --- BUF["BUF"]
  KC --- DEN["DEN"]
  BUF --- NE["NE"]
```

Throughout: **V** = \|vertices\|, **E** = \|edges\|, **deg(v)** = degree of vertex v.

---

## Graph types

| Type | Edge direction | Weight | NFL example |
| --- | --- | --- | --- |
| Undirected | Both ways | Optional | Mutual opponent link |
| Directed | One way | Optional | Coach → coordinator |
| Weighted | Either | On edge | Miles between stadiums |
| Unweighted | Either | 1 | Played in same week |
| Acyclic DAG | Directed, no cycles | — | Play prerequisite tree |
| Bipartite | Two partitions | — | Teams vs games |

---

## Representations compared

| Representation | Space | Edge query (u,v)? | Neighbors of u | Best when |
| --- | --- | --- | --- | --- |
| **Adjacency list** | O(V + E) | O(deg(u)) scan | O(deg(u)) | Sparse NFL schedules |
| **Adjacency matrix** | O(V²) | O(1) | O(V) | Dense tiny V (32 teams max still OK) |
| **Edge list** | O(E) | O(E) | O(E) | Kruskal MST, storage |

```mermaid
flowchart TB
  subgraph list["Adjacency list for KC"]
    KC2["KC → BUF, DEN, LAC"]
  end
  subgraph matrix["Matrix snippet"]
    M["M[KC][BUF] = 1"]
  end
```

---

## Ways to create a graph

### 1. Empty adjacency-list graph

```python
graph: dict[str, list[str]] = {}
```

### 2. Empty `Graph` class

```python
class Graph:
    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adj: dict[str, list[str]] = {}
```

### 3. From edge list — season games

```python
edges = [
    ("KC", "BAL"),
    ("BUF", "MIA"),
    ("KC", "BUF"),
]
g = Graph.from_edges(edges, directed=False)
```

| | |
| --- | --- |
| **Time** | O(E) |
| **Space** | O(V + E) |

### 4. From adjacency dict

```python
g = Graph.from_adjacency({
    "KC": ["BAL", "BUF"],
    "BAL": ["KC"],
    "BUF": ["KC"],
})
```

### 5. Weighted edges

```python
wg = WeightedGraph()
wg.add_edge("KC", "BUF", weight=1100)  # miles, teaching
```

---

## Reference implementation (adjacency list)

```python
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, Iterator


Vertex = Hashable


@dataclass
class Edge:
    u: Vertex
    v: Vertex
    weight: float = 1.0


class Graph:
    """Undirected or directed graph via adjacency lists."""

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adj: dict[Vertex, list[Vertex]] = {}

    @classmethod
    def from_edges(
        cls, edges: Iterable[tuple[Vertex, Vertex]], directed: bool = False
    ) -> Graph:
        g = cls(directed=directed)
        for u, v in edges:
            g.add_edge(u, v)
        return g

    def add_vertex(self, v: Vertex) -> None:
        self.adj.setdefault(v, [])

    def add_edge(self, u: Vertex, v: Vertex) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)
        else:
            self.adj.setdefault(v, [])

    def neighbors(self, v: Vertex) -> list[Vertex]:
        return self.adj.get(v, [])

    def vertices(self) -> list[Vertex]:
        return list(self.adj.keys())

    def edges_undirected_count(self) -> int:
        return sum(len(nbs) for nbs in self.adj.values()) // (
            1 if self.directed else 2
        )

    def bfs(self, start: Vertex) -> list[Vertex]:
        """Breadth-first order from start."""
        order: list[Vertex] = []
        seen = {start}
        q: deque[Vertex] = deque([start])
        while q:
            v = q.popleft()
            order.append(v)
            for w in self.neighbors(v):
                if w not in seen:
                    seen.add(w)
                    q.append(w)
        return order

    def dfs(self, start: Vertex) -> list[Vertex]:
        """Depth-first preorder from start."""
        order: list[Vertex] = []
        seen: set[Vertex] = set()

        def visit(v: Vertex) -> None:
            seen.add(v)
            order.append(v)
            for w in self.neighbors(v):
                if w not in seen:
                    visit(w)

        visit(start)
        return order

    def connected_components(self) -> list[list[Vertex]]:
        """Undirected components; treats as undirected if directed flag set."""
        seen: set[Vertex] = set()
        comps: list[list[Vertex]] = []
        for v in self.vertices():
            if v in seen:
                continue
            comp = self.bfs(v)
            comps.append(comp)
            seen.update(comp)
        return comps

    def has_path(self, src: Vertex, dst: Vertex) -> bool:
        return dst in set(self.bfs(src))


class WeightedGraph:
    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adj: dict[Vertex, list[tuple[Vertex, float]]] = {}

    def add_edge(self, u: Vertex, v: Vertex, weight: float = 1.0) -> None:
        self.adj.setdefault(u, []).append((v, weight))
        if not self.directed:
            self.adj.setdefault(v, []).append((u, weight))
        else:
            self.adj.setdefault(v, [])

    def dijkstra(self, src: Vertex) -> dict[Vertex, float]:
        import heapq

        dist: dict[Vertex, float] = {src: 0.0}
        pq: list[tuple[float, Vertex]] = [(0.0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist.get(u, float("inf")):
                continue
            for v, w in self.adj.get(u, []):
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist
```

| | |
| --- | --- |
| **Space** | O(V + E) adjacency lists |

---

## BFS — breadth-first search

**Idea:** Explore layer by layer—first all opponents one game away, then two, etc.

```mermaid
flowchart TB
  S["Start KC"] --> L1["BAL, DEN"]
  L1 --> L2["BUF via BAL"]
```

```python
schedule = Graph.from_edges([("KC", "BAL"), ("BAL", "BUF"), ("KC", "DEN")])
order = schedule.bfs("KC")  # ['KC', 'BAL', 'DEN', 'BUF'] order depends on adj order
```

| | |
| --- | --- |
| **Time** | O(V + E) |
| **Space** | O(V) queue + seen |

**NFL use:** fewest **hops** in schedule graph; broadcast “teams within 2 degrees of KC.”

---

## DFS — depth-first search

**Idea:** Go deep along one rivalry chain before backtracking.

```mermaid
flowchart TB
  KC --> BAL --> BUF --> NE
  KC --> DEN
```

```python
coach_tree = Graph(directed=True)
coach_tree.add_edge("HC", "OC")
coach_tree.add_edge("OC", "QB_coach")
order = coach_tree.dfs("HC")
```

| | |
| --- | --- |
| **Time** | O(V + E) |
| **Space** | O(V) stack (recursion or explicit) |

**NFL use:** detect cycles in dependency graph; enumerate coaching subtree.

---

## Traversal comparison

| | BFS | DFS |
| --- | --- | --- |
| **Structure** | Queue | Stack / recursion |
| **Shortest unweighted path** | Yes | No |
| **Memory on wide graph** | Can be large frontier | Linear path depth |
| **NFL metaphor** | Ripple through schedule | Drill into one branch |

```mermaid
sequenceDiagram
  participant Analyst
  participant G as schedule graph
  Analyst->>G: BFS from KC
  G-->>Analyst: layer 1 opponents
  G-->>Analyst: layer 2 opponents
  Analyst->>G: DFS from HC
  G-->>Analyst: deep coaching chain first
```

---

## All operations (NFL examples + complexity)

### `add_vertex` / `add_edge`

```python
g = Graph()
g.add_edge("KC", "BAL")  # regular-season game
```

| | |
| --- | --- |
| **Time** | O(1) amortized append |
| **Space** | O(1) new edge storage |

### `neighbors(v)` — opponents of KC

| | |
| --- | --- |
| **Time** | O(deg(v)) |
| **Space** | O(1) to return list ref |

### `bfs` / `dfs`

See above.

### `connected_components` — isolated schedule islands

```python
comps = schedule.connected_components()
# preseason split graphs, etc.
```

| | |
| --- | --- |
| **Time** | O(V + E) |
| **Space** | O(V) |

### `has_path` — can we reach BUF from KC?

| | |
| --- | --- |
| **Time** | O(V + E) |
| **Space** | O(V) |

### Dijkstra — weighted travel

```python
dist = wg.dijkstra("KC")
miles_to_buf = dist.get("BUF", float("inf"))
```

| | |
| --- | --- |
| **Time** | O((V + E) log V) with binary heap |
| **Space** | O(V) |

---

## NFL application: team relationship graph

Vertices = teams; undirected edge if they played in the season.

```python
def build_season_graph(games: list[dict]) -> Graph:
    g = Graph(directed=False)
    for row in games:
        g.add_edge(row["home"], row["away"])
    return g

g = build_season_graph(schedule_rows)
kc_opponents = g.neighbors("KC")
```

| | |
| --- | --- |
| **Time** | O(games) |
| **Space** | O(V + E) |

---

## NFL application: drive state machine (directed)

Vertices = `(down, yards_to_go_bucket)`; edge = play outcome.

```python
drive_g = Graph(directed=True)
drive_g.add_edge((1, 10), (2, 7))
drive_g.add_edge((2, 7), (1, 10))
path_exists = drive_g.has_path((1, 10), (4, 1))
```

---

## Topological sort (DAG) — prerequisite plays drill

When edges mean “concept A before concept B” in a teaching DAG:

```python
def topological_sort(g: Graph) -> list[Vertex]:
    """g must be a DAG (directed, acyclic)."""
    indeg = {v: 0 for v in g.vertices()}
    for u in g.vertices():
        for w in g.neighbors(u):
            indeg[w] = indeg.get(w, 0) + 1
    q = deque([v for v, d in indeg.items() if d == 0])
    order: list[Vertex] = []
    while q:
        v = q.popleft()
        order.append(v)
        for w in g.neighbors(v):
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    if len(order) != len(indeg):
        raise ValueError("cycle in graph")
    return order
```

| | |
| --- | --- |
| **Time** | O(V + E) |
| **Space** | O(V) |

---

## Python stdlib and ecosystem

| Tool | Role |
| --- | --- |
| `dict` + `list` | DIY adjacency list (this page) |
| `collections.deque` | BFS queue |
| `heapq` | Dijkstra priority queue |
| **networkx** (optional) | `pip install networkx` — production graph algos |

```python
# Optional: networkx for advanced metrics
import networkx as nx

G = nx.Graph()
G.add_edge("KC", "BAL")
nx.shortest_path(G, "KC", "BUF")
```

**Rule of thumb:** learn with **`Graph` class** above; use **networkx** for centrality, community detection, and large NFL network studies.

---

## Master complexity table

| Operation / algorithm | Time | Space |
| --- | --- | --- |
| Store graph (adj list) | O(V + E) | O(V + E) |
| Add edge | O(1) amortized | O(1) |
| List neighbors | O(deg(v)) | O(1) |
| BFS / DFS from one start | O(V + E) | O(V) |
| All components | O(V + E) | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |
| Topological sort | O(V + E) | O(V) |
| Adjacency matrix check edge | O(1) | O(V²) storage |

---

## When to pick which representation (NFL context)

```mermaid
flowchart TD
  Q([Relationship query?])
  Q --> S{Sparse E vs 32 teams?}
  S -->|sparse| AL["Adjacency list"]
  S -->|need all-pairs| AM["Matrix 32×32"]
  Q --> P{Shortest path weighted?}
  P -->|yes| D["WeightedGraph + Dijkstra"]
  P -->|no| B["BFS unweighted"]
```

| Scenario | Best tool |
| --- | --- |
| 272 games season edges | Adjacency list |
| All-pairs 32 teams | 32×32 matrix OK |
| Coach tree | Directed DFS |
| Stadium miles | Weighted + Dijkstra |

---

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Double-counting undirected edges | Wrong E | Store once or halve count |
| BFS for weighted shortest | Wrong answer | Dijkstra |
| DFS stack overflow on huge V | Recursion limit | Iterative DFS |
| Directed vs undirected mix | Wrong neighbors | Flag `directed` |
| Ignoring disconnected start | BFS misses vertices | Loop all components |

---

## Related pages

| Page | Relationship |
| --- | --- |
| [Sets](sets/index.md) | Vertices only, no edges |
| [Honorable mention ADT](honorable-mention-adt/index.md) | Union-Find for connectivity |
| [Queue](../queue/index.md) | BFS queue |
| [Priority queue](../priority-queue/index.md) | Dijkstra heap |
| [Complexity analysis](../../complexity/index.md) | O(V + E) notation |

---

## Quick reference card

```python
g = Graph()
g = Graph.from_edges([("KC", "BAL")], directed=False)

g.add_edge(u, v)
g.neighbors(v)
g.bfs(start)
g.dfs(start)
g.connected_components()
g.has_path(src, dst)

wg = WeightedGraph()
wg.add_edge(u, v, weight=1.0)
wg.dijkstra(src)
```

Use a **graph** when NFL questions are about **connections and paths**, not column means—use **pandas** for aggregations, **graphs** for topology.
