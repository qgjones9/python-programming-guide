"""
Climbing Stairs - Multiple Solutions

You are climbing a staircase. It takes n steps to reach the top.
Each time you can climb 1 or 2 steps. Return the number of distinct
ways to climb to the top.

Example:
    n = 4
    Output: 5

Author: python-programming-guide
"""


def climb_stairs_bottom_up(n):
    """
    Bottom-up DP: ways to reach step i = ways(i-1) + ways(i-2).

    Time Complexity: O(n)
    Space Complexity: O(n)

    Args:
        n (int): Number of stairs.

    Returns:
        int: Count of distinct paths to the top.

    Example:
        climb_stairs_bottom_up(4) -> 5
    """
    if n <= 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2

    for step in range(3, n + 1):
        dp[step] = dp[step - 1] + dp[step - 2]

    return dp[n]


def climb_stairs_memo(n):
    """
    Top-down DP with memoization on the same recurrence.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Args:
        n (int): Number of stairs.

    Returns:
        int: Count of distinct paths to the top.

    Example:
        climb_stairs_memo(4) -> 5
    """
    memo = {1: 1, 2: 2}

    def ways(steps):
        if steps in memo:
            return memo[steps]
        memo[steps] = ways(steps - 1) + ways(steps - 2)
        return memo[steps]

    return ways(n)


def climb_stairs_constant_space(n):
    """
    Bottom-up DP with only two rolling variables.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        n (int): Number of stairs.

    Returns:
        int: Count of distinct paths to the top.

    Example:
        climb_stairs_constant_space(4) -> 5
    """
    if n <= 2:
        return n

    prev_prev = 1
    prev = 2

    for _ in range(3, n + 1):
        current = prev_prev + prev
        prev_prev = prev
        prev = current

    return prev


def climb_stairs_brute_force(n):
    """
    Enumerate every 1-or-2 step choice recursively.

    Time Complexity: O(2^n)
    Space Complexity: O(n) call stack

    Args:
        n (int): Number of stairs.

    Returns:
        int: Count of distinct paths to the top.

    Example:
        climb_stairs_brute_force(4) -> 5
    """
    def count(remaining):
        if remaining <= 0:
            return 1 if remaining == 0 else 0
        return count(remaining - 1) + count(remaining - 2)

    return count(n)


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify walkthrough to test different cases.
    """
    walkthrough = 4
    print("Bottom-up DP:", climb_stairs_bottom_up(walkthrough))
    print("Top-down memo:", climb_stairs_memo(walkthrough))
    print("Constant space:", climb_stairs_constant_space(walkthrough))
    print("Brute force:", climb_stairs_brute_force(walkthrough))

    for case in (1, 2, 3, 5):
        print(
            f"n={case}:",
            climb_stairs_bottom_up(case),
            climb_stairs_memo(case),
            climb_stairs_constant_space(case),
        )
