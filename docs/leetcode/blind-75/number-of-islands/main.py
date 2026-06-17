"""
Number of Islands - Multiple Solutions

Given an m x n 2D grid of '1's (land) and '0's (water), return the number of
islands. An island is formed by adjacent land cells connected horizontally or
vertically.

Example:
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    Output: 3

Author: python-programming-guide
"""

import copy
from collections import deque


def num_islands_dfs(grid):
    """
    DFS flood fill: sink each discovered island in place.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n) worst-case recursion stack

    Args:
        grid (List[List[str]]): Mutable grid of '0' and '1'.

    Returns:
        int: Number of islands.

    Example:
        num_islands_dfs([["1", "0"], ["0", "1"]]) -> 2
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def sink(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)

    return count


def num_islands_bfs(grid):
    """
    BFS flood fill: queue expands each island; marks visited in place.

    Time Complexity: O(m * n)
    Space Complexity: O(min(m, n)) queue size in typical grids

    Args:
        grid (List[List[str]]): Mutable grid of '0' and '1'.

    Returns:
        int: Number of islands.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            count += 1
            queue = deque([(r, c)])
            grid[r][c] = "0"
            while queue:
                row, col = queue.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = row + dr, col + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] == "1"
                    ):
                        grid[nr][nc] = "0"
                        queue.append((nr, nc))

    return count


def num_islands_union_find(grid):
    """
    Union-Find: union each land cell with land neighbors to the left and above.

    Time Complexity: O(m * n * alpha(m * n))
    Space Complexity: O(m * n)

    Args:
        grid (List[List[str]]): Grid of '0' and '1' (not mutated).

    Returns:
        int: Number of islands.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    parent = {}
    count = 0

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(a, b):
        root_a, root_b = find(a), find(b)
        if root_a == root_b:
            return False
        parent[root_b] = root_a
        return True

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            idx = r * cols + c
            parent[idx] = idx
            count += 1
            if c > 0 and grid[r][c - 1] == "1":
                if union(idx, idx - 1):
                    count -= 1
            if r > 0 and grid[r - 1][c] == "1":
                if union(idx, idx - cols):
                    count -= 1

    return count


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify walkthrough to test different cases.
    """
    walkthrough = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    print("DFS:", num_islands_dfs(copy.deepcopy(walkthrough)))
    print("BFS:", num_islands_bfs(copy.deepcopy(walkthrough)))
    print("Union-Find:", num_islands_union_find(copy.deepcopy(walkthrough)))
