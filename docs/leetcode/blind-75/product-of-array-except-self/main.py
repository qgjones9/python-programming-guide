"""
Product of Array Except Self - Multiple Solutions

Given an integer array nums, return an array answer such that answer[i] is
equal to the product of all elements except nums[i]. Solve in O(n) time
without using division.

Example:
    nums = [1, 2, 3, 4]
    Output: [24, 12, 8, 6]

Author: python-programming-guide
"""


def product_except_self(nums):
    """
    Two-pass solution: prefix products in answer, then multiply suffix.

    Time Complexity: O(n)
    Space Complexity: O(1) extra (output array excluded)

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


def product_except_self_prefix_suffix(nums):
    """
    Build explicit prefix and suffix arrays, then multiply element-wise.

    Time Complexity: O(n)
    Space Complexity: O(n)

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
