"""
Container With Most Water - Multiple Solutions

Given n non-negative integers representing vertical line heights, find two
lines that form a container holding the most water.

Example:
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    Output: 49  (lines at indices 1 and 8)

Author: python-programming-guide
"""


def max_area_two_pointers(height):
    """
    Two pointers from both ends; move the shorter line inward each step.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        height (List[int]): Line heights indexed left to right.

    Returns:
        int: Maximum water area between any two lines.

    Example:
        max_area_two_pointers([1, 8, 6, 2, 5, 4, 8, 3, 7]) -> 49
    """
    left = 0
    right = len(height) - 1
    best = 0

    while left < right:
        width = right - left
        bounded_height = min(height[left], height[right])
        best = max(best, width * bounded_height)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best


def max_area_brute_force(height):
    """
    Try every pair of lines and keep the maximum area.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    Args:
        height (List[int]): Line heights indexed left to right.

    Returns:
        int: Maximum water area between any two lines.

    Example:
        max_area_brute_force([1, 8, 6, 2, 5, 4, 8, 3, 7]) -> 49
    """
    best = 0
    n = len(height)

    for left in range(n):
        for right in range(left + 1, n):
            width = right - left
            bounded_height = min(height[left], height[right])
            best = max(best, width * bounded_height)

    return best


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify walkthrough to test different cases.
    """
    walkthrough = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print("Two Pointers:", max_area_two_pointers(walkthrough))
    print("Brute Force:", max_area_brute_force(walkthrough))
