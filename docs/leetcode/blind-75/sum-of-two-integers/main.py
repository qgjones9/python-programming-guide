"""
Sum of Two Integers - Multiple Solutions

Given two integers a and b, return their sum without using + or - operators.

Example:
    a = 1, b = 2
    Output: 3

Author: python-programming-guide
"""

MASK = 0xFFFFFFFF
MAX_INT = 0x7FFFFFFF


def _to_signed(value):
    """Convert an unsigned 32-bit value to a signed Python int."""
    return value if value <= MAX_INT else ~(value ^ MASK)


def get_sum_bitwise(a, b):
    """
    Add two integers with XOR (sum without carry) and AND+shift (carry).

    Time Complexity: O(1) — at most 32 iterations for 32-bit integers
    Space Complexity: O(1)

    Args:
        a (int): First addend.
        b (int): Second addend.

    Returns:
        int: a + b without using + or -.

    Example:
        get_sum_bitwise(1, 2) -> 3
        get_sum_bitwise(5, 14) -> 19
        get_sum_bitwise(-20, -30) -> -50
    """
    a, b = a & MASK, b & MASK
    while b:
        carry = ((a & b) << 1) & MASK
        a, b = (a ^ b) & MASK, carry
    return _to_signed(a)


def get_sum_recursive(a, b):
    """
    Recursive bitwise add: base case when carry is zero.

    Time Complexity: O(1) — at most 32 recursive calls
    Space Complexity: O(1) — tail-recursion depth bounded by bit width

    Args:
        a (int): First addend.
        b (int): Second addend.

    Returns:
        int: a + b without using + or -.

    Example:
        get_sum_recursive(37, 62) -> 99
    """
    a, b = a & MASK, b & MASK
    if b == 0:
        return _to_signed(a)
    carry = ((a & b) << 1) & MASK
    return get_sum_recursive((a ^ b) & MASK, carry)


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify walkthrough_a and walkthrough_b to test different cases.
    """
    walkthrough_a = 5
    walkthrough_b = 14
    print("Bitwise:", get_sum_bitwise(walkthrough_a, walkthrough_b))
    print("Recursive:", get_sum_recursive(walkthrough_a, walkthrough_b))

    print("LeetCode ex1:", get_sum_bitwise(1, 2))
    print("LeetCode ex2:", get_sum_bitwise(2, 3))
    print("Negatives:", get_sum_bitwise(-20, -30))
    print("Large pair:", get_sum_bitwise(37, 62))
