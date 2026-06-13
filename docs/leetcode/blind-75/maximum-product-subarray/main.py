"""
Maximum Product Subarray - Multiple Solutions

Given an integer array nums, find a contiguous subarray that has the largest
product and return that product.

Example:
    nums = [2, 3, -2, 4]
    Output: 6  (subarray [2, 3])

Author: python-programming-guide
"""


def max_product_subarray(nums):
    """
    Min/max running products: track best and worst product ending at each index.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        int: Largest product of any contiguous subarray.

    Example:
        max_product_subarray([2, 3, -2, 4]) -> 6
    """
    result = nums[0]
    cur_min = cur_max = 1

    for n in nums:
        if n == 0:
            result = max(result, 0)
            cur_min = cur_max = 1
            continue

        tmp_max = max(n, n * cur_max, n * cur_min)
        tmp_min = min(n, n * cur_max, n * cur_min)
        cur_max, cur_min = tmp_max, tmp_min
        result = max(result, cur_max)

    return result


def max_product_subarray_brute_force(nums):
    """
    Brute force: multiply every contiguous subarray and keep the maximum.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        int: Largest product of any contiguous subarray.

    Example:
        max_product_subarray_brute_force([2, 3, -2, 4]) -> 6
    """
    best = nums[0]

    for start in range(len(nums)):
        running = 1
        for end in range(start, len(nums)):
            running *= nums[end]
            best = max(best, running)

    return best


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify nums to test different cases.
    """
    leetcode_1 = [2, 3, -2, 4]
    leetcode_2 = [-2, 0, -1]
    walkthrough = [-1, -2, -3, 0, 3, 5, -1, -2]

    print("LeetCode example 1:", max_product_subarray(leetcode_1))
    print("LeetCode example 2:", max_product_subarray(leetcode_2))
    print("Walkthrough input:", max_product_subarray(walkthrough))

    print("Brute force (example 1):", max_product_subarray_brute_force(leetcode_1))
    print("Brute force (walkthrough):", max_product_subarray_brute_force(walkthrough))
