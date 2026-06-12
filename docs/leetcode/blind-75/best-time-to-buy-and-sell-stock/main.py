"""
Best Time to Buy and Sell Stock - Multiple Solutions

Given an array `prices` where prices[i] is the stock price on day i, find the
maximum profit from one buy and one sell (sell must occur after buy).
Return 0 if no profit is possible.

Example:
    prices = [7, 1, 5, 3, 6, 4]
    Output: 5  (buy at 1, sell at 6)

Author: python-programming-guide
"""


def max_profit_one_pass(prices):
    """
    One-pass solution: track the minimum buy price seen so far.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        prices (List[int]): Daily stock prices.

    Returns:
        int: Maximum profit from one buy and one sell, or 0.

    Example:
        max_profit_one_pass([7, 1, 5, 3, 6, 4]) -> 5
    """
    if not prices:
        return 0

    min_price = prices[0]
    max_profit = 0

    for price in prices[1:]:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit


def max_profit_brute_force(prices):
    """
    Brute force: for each buy day, find the maximum sell price on the right.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    Args:
        prices (List[int]): Daily stock prices.

    Returns:
        int: Maximum profit from one buy and one sell, or 0.

    Example:
        max_profit_brute_force([7, 1, 5, 3, 6, 4]) -> 5
    """
    max_profit = 0

    for buy in range(len(prices)):
        max_sell = prices[buy]
        for sell in range(buy + 1, len(prices)):
            max_sell = max(max_sell, prices[sell])
        max_profit = max(max_profit, max_sell - prices[buy])

    return max_profit


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify prices to test different cases.
    """
    prices = [7, 1, 5, 3, 6, 4]
    print("One Pass:", max_profit_one_pass(prices))
    print("Brute Force:", max_profit_brute_force(prices))
