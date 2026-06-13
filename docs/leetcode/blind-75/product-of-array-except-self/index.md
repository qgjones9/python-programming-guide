# [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self)

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a **32-bit integer**.

You must write an algorithm that runs in **O(n)** time and **without using the division operator**.

## Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]

## Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

## Constraints:

`2` <= `nums.length` <= `10^5`
`-30` <= `nums[i]` <= `30`
The input is generated such that `answer[i]` is guaranteed to fit in a 32-bit integer.

*Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space.)*


## Approach

For each index `i`, you need the product of everything **left** of `i` times everything **right** of `i`. Division would make this trivial—multiply all elements, then divide out `nums[i]`—but the problem forbids division. The interview path is **prefix products** and **suffix products**.

### Why not division?

If division were allowed, compute the total product of all elements, then set `answer[i] = total / nums[i]`. For `nums = [1, 2, 3, 4]`, total is `24`, and dividing by each element gives `[24, 12, 8, 6]`. Zeros and negatives make division fragile, and LeetCode disallows it here—so use multiplication-only logic instead.

### Prefix and suffix products

For each index, split the "everyone except me" product into two parts:

| Term | Meaning |
|------|---------|
| **Prefix product** | Product of all elements to the **left** of `i` |
| **Suffix product** | Product of all elements to the **right** of `i` |

Then:

$$
\text{answer}[i] = \text{prefix}[i] \times \text{suffix}[i]
$$

For `nums = [1, 2, 3, 4]`:

| Index | `nums[i]` | Prefix (left product) | Suffix (right product) | `answer[i]` |
|-------|-----------|------------------------|------------------------|-------------|
| 0 | 1 | 1 | 2 × 3 × 4 = 24 | 24 |
| 1 | 2 | 1 | 3 × 4 = 12 | 12 |
| 2 | 3 | 1 × 2 = 2 | 4 | 8 |
| 3 | 4 | 1 × 2 × 3 = 6 | 1 | 6 |

Prefix array: `[1, 1, 2, 6]`. Suffix array: `[24, 12, 4, 1]`. Element-wise multiply → `[24, 12, 8, 6]`.

The same idea works with zeros and negatives—for example `nums = [-1, 1, 0, -3, 3]`—because each answer is built from explicit left and right products, not division.

### Two arrays: clear but O(n) extra space

Build separate `prefix` and `suffix` arrays in two passes, then combine. Time is O(n); extra space is O(n) beyond the output.

### Optimized: one output array + suffix variable

You can drop the suffix array:

| Step | Action |
|------|--------|
| 1 | Initialize `answer` and fill it with **prefix products** left to right, using a running `prefix` variable starting at `1`. |
| 2 | Walk **right to left** with a running `suffix` variable starting at `1`. |
| 3 | At each index, multiply `answer[i]` (already the prefix) by `suffix`, then update `suffix *= nums[i]`. |

Only one extra variable is needed besides the output array—O(n) time and **O(1) extra space** (output excluded).

### Walkthrough: optimized two-pass on `nums = [1, 2, 3, 4]`

**Pass 1 — prefix into `answer`:**

| Index | `prefix` before | `answer[i]` | `prefix` after |
|-------|-----------------|-------------|----------------|
| 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 2 |
| 2 | 2 | 2 | 6 |
| 3 | 6 | 6 | 24 |

After pass 1: `answer = [1, 1, 2, 6]`.

**Pass 2 — multiply suffix:**

| Index | `suffix` before | `answer[i]` after | `suffix` after |
|-------|-----------------|-------------------|----------------|
| 3 | 1 | 6 × 1 = 6 | 4 |
| 2 | 4 | 2 × 4 = 8 | 12 |
| 1 | 12 | 1 × 12 = 12 | 24 |
| 0 | 24 | 1 × 24 = 24 | 24 |

Final answer: `[24, 12, 8, 6]`.

### Complexity of the optimized approach

| Time | Space | Why |
|------|-------|-----|
| O(n) | O(1) extra | Two linear passes; only `prefix`/`suffix` running variables besides output |

The implementations below lead with the optimized two-pass solution, then show the separate prefix/suffix arrays version for clarity.

## Implementation

Runnable code: [main.py](main.py)

## Solution 1: Two-Pass with Running Products (Best for Interview)

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n)            | O(1) extra       |

```python
def product_except_self(nums):
    """
    Two-pass solution: prefix products in answer, then multiply suffix.

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        List[int]: Product of all elements except self at each index.

    Example:
        product_except_self([1, 2, 3, 4]) -> [24, 12, 8, 6]
    """
    n = len(nums)
    answer = [1] * n

    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer
```

```java
public class ProductExceptSelf {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] answer = new int[n];

        int prefix = 1;
        for (int i = 0; i < n; i++) {
            answer[i] = prefix;
            prefix *= nums[i];
        }

        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) {
            answer[i] *= suffix;
            suffix *= nums[i];
        }

        return answer;
    }
}
```

## Solution 2: Separate Prefix and Suffix Arrays

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n)            | O(n) extra       |

```python
def product_except_self_prefix_suffix(nums):
    """
    Build explicit prefix and suffix arrays, then multiply element-wise.

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        List[int]: Product of all elements except self at each index.

    Example:
        product_except_self_prefix_suffix([1, 2, 3, 4]) -> [24, 12, 8, 6]
    """
    n = len(nums)
    prefix = [1] * n
    suffix = [1] * n

    for i in range(1, n):
        prefix[i] = prefix[i - 1] * nums[i - 1]

    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i + 1] * nums[i + 1]

    return [prefix[i] * suffix[i] for i in range(n)]
```

## Summary

Run both approaches with the same input:

```python
if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify nums to test different cases.
    """
    nums = [1, 2, 3, 4]
    print("Two Pass:", product_except_self(nums))
    print("Prefix/Suffix Arrays:", product_except_self_prefix_suffix(nums))

    nums_with_zero = [-1, 1, 0, -3, 3]
    print("Two Pass (zeros):", product_except_self(nums_with_zero))
    print("Prefix/Suffix (zeros):", product_except_self_prefix_suffix(nums_with_zero))
```

## Internal References

- [Maximum Product Subarray](../maximum-product-subarray/index.md) — another array product pattern; contiguous max product vs prefix/suffix "except self".
- [Maximum Subarray](../maximum-subarray/index.md) — contiguous subarray with **sum** instead of product (Kadane).
