# [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock)

You are given an array `prices` where `prices[i]` is the price of a stock on day `i`.

You want to maximize profit by choosing **one day to buy** and **a different day in the future to sell**. You may complete at most **one transaction** (buy once and sell once).

Return the maximum profit you can achieve. If no profit is possible, return `0`.

## Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 - 1 = 5.

## Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: Prices only decrease, so no profitable transaction exists.

## Constraints:

`1` <= `prices.length` <= `10^5`
`0` <= `prices[i]` <= `10^4`


## Approach

You need the largest positive difference `prices[sell] - prices[buy]` where `sell > buy`. Start with the obvious baseline—try every buy day and look right for the best sell—then upgrade to a single left-to-right pass that tracks the cheapest buy so far. That second approach is what you should reach for in an interview.

### Brute force: buy day + max price on the right

The simplest idea is to fix each day as a buy day, scan every later day for the highest sell price, and keep the best profit. Initialize `max_profit = 0` so a decreasing array correctly returns `0`.

| Aspect | Detail |
|--------|--------|
| Time | O(n²) — for each buy day, scan the suffix |
| Space | O(1) — only loop variables and running max |
| Drawback | Too slow when `n` is large |

For `prices = [7, 1, 5, 3, 6, 4]`, buying at `7` yields negative profits; buying at `1` and selling at `6` gives `5`, which is the answer.

### One pass: track minimum buy price

You can do better by scanning left to right **once**. At each price, ask: *if I sell today, what is the best profit using the cheapest buy price seen so far?*

Maintain two variables:

| Variable | Role |
|----------|------|
| `min_price` | Lowest price seen on any earlier day (best buy so far) |
| `max_profit` | Best profit achievable up to the current day |

For a current price `p`:

$$
\text{profit\_today} = p - \text{min\_price}
$$

Update `max_profit = max(max_profit, profit_today)` and `min_price = min(min_price, p)`.

| Step | Action |
|------|--------|
| 0 | Set `min_price = prices[0]` and `max_profit = 0`. |
| 1 | Walk `prices` from left to right (or start at index `1` after seeding `min_price`). |
| 2 | Before using today's price as a sell, update `min_price` if today is cheaper. |
| 3 | Compute `profit_today = price - min_price`. |
| 4 | Update `max_profit = max(max_profit, profit_today)`. |
| 5 | Return `max_profit`. |

Because you only need the **minimum prefix price**, not every past price, this is O(n) time and O(1) space—the classic single-scan optimization.

### Walkthrough: `prices = [7, 1, 5, 3, 6, 4]`

| Day | Price | `min_price` after update | Profit if sell today | `max_profit` |
|-----|-------|--------------------------|----------------------|--------------|
| 0 | 7 | 7 | 0 | 0 |
| 1 | 1 | 1 | 1 − 7 → capped at 0 | 0 |
| 2 | 5 | 1 | 4 | 4 |
| 3 | 3 | 1 | 2 | 4 |
| 4 | 6 | 1 | 5 | 5 |
| 5 | 4 | 1 | 3 | 5 |

The best transaction is buy at `1`, sell at `6`, for profit `5`. On a strictly decreasing array like `[7, 6, 4, 3, 1]`, every `profit_today` is negative and `max_profit` stays `0`.

### Complexity of the one-pass approach

| Time | Space | Why |
|------|-------|-----|
| O(n) | O(1) | One left-to-right pass; only `min_price` and `max_profit` are stored |

The implementations below lead with the one-pass solution, then show brute force so you can compare trade-offs side by side.

## Solution 1: One Pass (Best for Interview)

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n)            | O(1)             |

```python
def max_profit_one_pass(prices):
    """
    One-pass solution: track the minimum buy price seen so far.

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
```

```java
public class MaxProfit {
    public int maxProfit(int[] prices) {
        if (prices.length == 0) {
            return 0;
        }
        int minPrice = prices[0];
        int maxProfit = 0;
        for (int i = 1; i < prices.length; i++) {
            minPrice = Math.min(minPrice, prices[i]);
            maxProfit = Math.max(maxProfit, prices[i] - minPrice);
        }
        return maxProfit;
    }
}
```

## Solution 2: Brute Force

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n^2)          | O(1)             |

```python
def max_profit_brute_force(prices):
    """
    Brute force: for each buy day, find the maximum sell price on the right.

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
```

## Summary

Run both approaches with the same input:

```python
if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify prices to test different cases.
    """
    prices = [7, 1, 5, 3, 6, 4]
    print("One Pass:", max_profit_one_pass(prices))
    print("Brute Force:", max_profit_brute_force(prices))
```
