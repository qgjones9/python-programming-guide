"""
Coin Change - Multiple Solutions

You are given an integer array coins representing coin denominations and an
integer amount representing a total amount of money. Return the fewest number
of coins needed to make up that amount, or -1 if it is impossible.

Example:
    coins = [1, 2, 5], amount = 11
    Output: 3  (5 + 5 + 1)

Author: python-programming-guide
"""


def coin_change_bottom_up(coins, amount):
    """
    Bottom-up DP: dp[i] = minimum coins to form amount i.

    Time Complexity: O(amount * len(coins))
    Space Complexity: O(amount)

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


def coin_change_memo(coins, amount):
    """
    Top-down DP with memoization on the same recurrence.

    Time Complexity: O(amount * len(coins))
    Space Complexity: O(amount)

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


def coin_change_bfs(coins, amount):
    """
    BFS from amount down to 0 — each subtraction is one edge.

    Time Complexity: O(amount * len(coins))
    Space Complexity: O(amount)

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


def coin_change_brute_force(coins, amount):
    """
    Try every coin at each remaining amount recursively.

    Time Complexity: O(len(coins) ^ amount) in the worst case
    Space Complexity: O(amount) call stack

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

    cases = [
        ([1, 2, 5], 11, 3),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1, 3, 4], 6, 2),
    ]
    for coins, amount, expected in cases:
        got = coin_change_bottom_up(coins, amount)
        assert got == expected, f"coins={coins}, amount={amount}: expected {expected}, got {got}"
        assert coin_change_memo(coins, amount) == expected
        assert coin_change_bfs(coins, amount) == expected
    print("All LeetCode examples and edge cases passed.")
