# [Coin Change](https://leetcode.com/problems/coin-change/)

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the **fewest number of coins** that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.

You may assume that you have an infinite number of each kind of coin.

## Example 1:

Input: coins = `[1,2,5]`, amount = `11`
Output: `3`
Explanation: `11 = 5 + 5 + 1`

## Example 2:

Input: coins = `[2]`, amount = `3`
Output: `-1`

## Example 3:

Input: coins = `[1]`, amount = `0`
Output: `0`

## Constraints:

- `1 <= coins.length <= 12`
- `1 <= coins[i] <= 2^31 - 1`
- `0 <= amount <= 10^4`


## :material-school: What you'll learn

!!! abstract "Learning objectives"
    You will model minimum-coin change as unbounded knapsack DP, build the answer bottom-up in one pass, and explain why greedy coin picking fails on classic counterexamples.


## Worked example data

Primary input for the amount-by-amount trace below:

```text
# primary walkthrough input
coins = [1, 2, 5]
amount = 11
# expected output: 3  (5 + 5 + 1)
```

| Example | Notes | Answer |
|---------|-------|--------|
| `coins = [1,2,5]`, `amount = 11` | Full walkthrough below | `3` |
| `coins = [2]`, `amount = 3` | Odd target, only even coins | `-1` |
| `coins = [1]`, `amount = 0` | Zero base case | `0` |
| `coins = [1,3,4]`, `amount = 6` | Greedy trap (see Approach) | `2` |


## Approach

You need the **minimum number of coins** to reach exactly `amount`, with unlimited use of each denomination. Start with brute-force recursion that tries every coin at each step, then replace overlapping subproblems with bottom-up DP—the pattern you should reach for in an interview.

### Brute force: try every coin at each remaining amount

At each remaining value, subtract one coin and recurse on what is left. Track the minimum chain length that hits zero.

| Aspect | Detail |
|--------|--------|
| Time | Exponential — branching factor is `len(coins)` per level |
| Space | O(amount) — recursion depth |
| Drawback | Recomputes the same sub-amounts many times |

For `coins = [1, 2, 5]` and `amount = 11`, one optimal path is `11 → 6 → 1 → 0` using coins `5, 5, 1` — three coins total.

### Greedy does not work here

💡 A natural wrong turn is “always take the largest coin that fits.” That works for US change with `{1, 5, 10, 25}` but **not** for arbitrary denominations.

| Step | Greedy on `[1,3,4]`, amount `6` | Optimal |
|------|----------------------------------|---------|
| 1 | Take `4` → remaining `2` | Take `3` → remaining `3` |
| 2 | Take `1` → remaining `1` | Take `3` → remaining `0` |
| 3 | Take `1` → remaining `0` | Done |
| Total | **3** coins | **2** coins (`3 + 3`) |

!!! warning "Interview trap: do not greedily pick the largest coin"
    Largest-first greedy can miss the global minimum. For `coins = [1, 3, 4]` and `amount = 6`, greedy yields three coins (`4 + 1 + 1`) while DP finds two (`3 + 3`). State the DP recurrence instead of assuming canonical currency.

### Bottom-up DP: `dp[i]` = fewest coins to make amount `i`

For each amount `i` from `1` to `amount`, consider every coin `c` where `c <= i`. The best way to form `i` is one coin `c` plus the best way to form `i - c`:

$$
\text{dp}[i] = \min_{c \in \text{coins},\ c \le i}\bigl(\text{dp}[i - c] + 1\bigr)
$$

| Variable | Role |
|----------|------|
| `dp[i]` | Minimum coins needed to make exactly amount `i` |
| `dp[0]` | Base case: zero coins for amount `0` |
| Sentinel | Initialize unreachable slots to `amount + 1` (more than any valid answer) |

| Step | Action |
|------|--------|
| 0 | If `amount == 0`, return `0`. |
| 1 | Set `dp[0] = 0`; fill `dp[1..amount]` with sentinel `amount + 1`. |
| 2 | For `i` from `1` to `amount`, for each `coin`, if `coin <= i`, update `dp[i]`. |
| 3 | Return `dp[amount]` if reachable, else `-1`. |

!!! info "Unbounded knapsack recurrence"
    Each coin can be reused, so when you relax `dp[i]` with coin `c`, you read `dp[i - c]` from the **same** row—already computed for a smaller amount. You are minimizing count, not maximizing value.

```mermaid
flowchart TD
    A[amount == 0?] -->|yes| B[Return 0]
    A -->|no| C[dp0 = 0, rest = sentinel]
    C --> D[i = 1 to amount]
    D --> E[For each coin c where c <= i]
    E --> F["dp[i] = min(dp[i], dp[i-c] + 1)"]
    F --> G{i == amount?}
    G -->|no| D
    G -->|yes| H{dp[amount] reachable?}
    H -->|yes| I[Return dp[amount]]
    H -->|no| J[Return -1]
```

### Walkthrough: `coins = [1, 2, 5]`, `amount = 11`

| Amount `i` | Best choice | `dp[i]` |
|------------|-------------|---------|
| 0 | — | 0 |
| 1 | `1` | 1 |
| 2 | `2` | 1 |
| 3 | `2 + 1` | 2 |
| 4 | `2 + 2` | 2 |
| 5 | `5` | 1 |
| 6 | `5 + 1` | 2 |
| 7 | `5 + 2` | 2 |
| 8 | `5 + 2 + 1` | 3 |
| 9 | `5 + 2 + 2` | 3 |
| 10 | `5 + 5` | 2 |
| 11 | `5 + 5 + 1` | **3** |

Three coins — `5 + 5 + 1` — matches Example 1.

!!! success "Walkthrough confirmed"
    `dp[11] = 3`. The table shows why a five-cent coin at amount `5` drops the count to one, and combining two fives at amount `10` sets up the final one-cent finish.

### Top-down memoization (same recurrence)

Define `min_coins(r)` = fewest coins to make remaining amount `r`. Then `min_coins(r) = min over coins of (min_coins(r - coin) + 1)` with base `min_coins(0) = 0`. Memoize each `r` once — same O(amount × coins) time as bottom-up, useful when you think recursively first.

### BFS on amounts (alternative optimal)

Treat each amount as a node. From `current`, subtract each coin to reach `current - coin`. First time you hit `0`, the layer count is the answer. Same asymptotic bounds; good when you want a shortest-path story without writing a recurrence.

| Approach | Time | Space |
|----------|------|-------|
| Brute force recursion | Exponential | O(amount) stack |
| Top-down memo | O(amount × \|coins\|) | O(amount) |
| Bottom-up array | O(amount × \|coins\|) | O(amount) |
| BFS on amounts | O(amount × \|coins\|) | O(amount) |

## Implementation

Runnable code: [main.py](main.py)

🎯 Lead with bottom-up DP in an interview—state `dp[i]` as min coins for amount `i`, write the recurrence, fill a small table, then mention greedy fails on `[1,3,4]` / `6`.

## Solution 1: Bottom-Up Dynamic Programming (Best for Interview)

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(amount × \|coins\|) | O(amount) |

```python
def coin_change_bottom_up(coins, amount):
    """
    Bottom-up DP: dp[i] = minimum coins to form amount i.

    Args:
        coins (list[int]): Available coin denominations.
        amount (int): Target amount.

    Returns:
        int: Fewest coins needed, or -1 if impossible.

    Example:
        coin_change_bottom_up([1, 2, 5], 11) -> 3
    """
    if amount == 0:
        return 0

    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0

    for current in range(1, amount + 1):
        for coin in coins:
            if coin <= current:
                dp[current] = min(dp[current], dp[current - coin] + 1)

    return dp[amount] if dp[amount] != unreachable else -1
```

```java
class Solution {
    public int coinChange(int[] coins, int amount) {
        if (amount == 0) {
            return 0;
        }
        int unreachable = amount + 1;
        int[] dp = new int[amount + 1];
        for (int i = 1; i <= amount; i++) {
            dp[i] = unreachable;
        }
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        return dp[amount] == unreachable ? -1 : dp[amount];
    }
}
```

## Solution 2: Top-Down Memoization

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(amount × \|coins\|) | O(amount) |

Same recurrence as Solution 1; natural if you frame the problem as “what is the minimum from here?”

```python
def coin_change_memo(coins, amount):
    """
    Top-down DP with memoization on the same recurrence.

    Args:
        coins (list[int]): Available coin denominations.
        amount (int): Target amount.

    Returns:
        int: Fewest coins needed, or -1 if impossible.

    Example:
        coin_change_memo([1, 2, 5], 11) -> 3
    """
    memo = {0: 0}

    def min_coins(remaining):
        if remaining in memo:
            return memo[remaining]
        if remaining < 0:
            return float("inf")

        best = float("inf")
        for coin in coins:
            best = min(best, min_coins(remaining - coin) + 1)

        memo[remaining] = best
        return best

    result = min_coins(amount)
    return result if result != float("inf") else -1
```

## Solution 3: BFS on Amounts

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(amount × \|coins\|) | O(amount) |

Shortest-path view: each subtraction is one step toward zero.

```python
def coin_change_bfs(coins, amount):
    """
    BFS from amount down to 0 — each subtraction is one edge.

    Args:
        coins (list[int]): Available coin denominations.
        amount (int): Target amount.

    Returns:
        int: Fewest coins needed, or -1 if impossible.

    Example:
        coin_change_bfs([1, 2, 5], 11) -> 3
    """
    if amount == 0:
        return 0

    from collections import deque

    queue = deque([(amount, 0)])
    visited = {amount}

    while queue:
        current, steps = queue.popleft()
        for coin in coins:
            next_amount = current - coin
            if next_amount == 0:
                return steps + 1
            if next_amount > 0 and next_amount not in visited:
                visited.add(next_amount)
                queue.append((next_amount, steps + 1))

    return -1
```

## Solution 4: Brute Force Recursion

| Time Complexity | Space Complexity |
|-----------------|------------------|
| Exponential | O(amount) |

Correct for tiny amounts; use only to motivate memoization or DP.

```python
def coin_change_brute_force(coins, amount):
    """
    Try every coin at each remaining amount recursively.

    Args:
        coins (list[int]): Available coin denominations.
        amount (int): Target amount.

    Returns:
        int: Fewest coins needed, or -1 if impossible.

    Example:
        coin_change_brute_force([1, 2, 5], 11) -> 3
    """
    if amount == 0:
        return 0

    best = float("inf")
    for coin in coins:
        if coin <= amount:
            sub = coin_change_brute_force(coins, amount - coin)
            if sub != -1:
                best = min(best, sub + 1)

    return best if best != float("inf") else -1
```

## Summary

Run all approaches with the same input:

```python
if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify walkthrough to test different cases.
    """
    walkthrough_coins = [1, 2, 5]
    walkthrough_amount = 11
    print("Bottom-up DP:", coin_change_bottom_up(walkthrough_coins, walkthrough_amount))
    print("Top-down memo:", coin_change_memo(walkthrough_coins, walkthrough_amount))
    print("BFS:", coin_change_bfs(walkthrough_coins, walkthrough_amount))
    print("Brute force:", coin_change_brute_force(walkthrough_coins, walkthrough_amount))
```

## Industry scenarios

- 📈 **Cash drawers:** Minimize physical coins returned as change when denominations are configurable per region.
- 🎮 **In-game currency:** Fewest token types to spend for an exact shop price with unlimited stack sizes.
- 📡 **Bandwidth packs:** Minimum number of fixed-size data bundles that sum to a target quota.


## :material-lightbulb: Key takeaways

- 🔑 Recurrence: `dp[i] = min(dp[i - coin] + 1)` over all usable coins — unbounded reuse.
- ⚡ Bottom-up or memoized top-down: O(amount × \|coins\|) time; sentinel `amount + 1` marks unreachable states.
- 🧩 `amount = 0` → `0`; impossible targets stay at sentinel → return `-1`.
- 💡 Greedy largest-coin-first fails on `[1, 3, 4]` with amount `6` — always justify DP.


## Internal References

- 🔗 [Climbing Stairs](../climbing-stairs/index.md) — simpler 1-or-2 step counting with the same bottom-up DP shape.
- 🔗 [Combination Sum](../combination-sum/index.md) — unbounded coin use with a different optimization goal.
- 🔗 [House Robber](../house-robber/index.md) — linear DP with local choices at each index.


## External References

- :fontawesome-solid-link: [Coin Change — LeetCode #322](https://leetcode.com/problems/coin-change/)
