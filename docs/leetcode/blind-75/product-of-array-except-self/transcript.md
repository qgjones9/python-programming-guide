# Product of Array Except Self


Let's solve the "Product of Array Except Self" coding interview question. Here is the problem statement: Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`. Each prefix and suffix product is guaranteed to fit in a 32-bit integer (so we don't have to worry about overflow). We are required to design an algorithm that runs in O(n) time complexity, and we cannot use the division operator.

Let's look at an example: `Input: nums = [1, 2, 3, 4]`. We need to return an array where each element is the product of the entire array except for the element at that position. For `nums[0]`, which is 1, the product of the other elements is `2 * 3 * 4 = 24`, so the first element of the output should be 24. For `nums[1]` (which is 2), the product of the other elements is `1 * 3 * 4 = 12`. For `nums[2]` (3), the product is `1 * 2 * 4 = 8`. For `nums[3]` (4), the product is `1 * 2 * 3 = 6`. Therefore, the output is `[24, 12, 8, 6]`.

In some cases, you may have zeros or negative numbers. For example, consider `nums = [-1, 1, 0, -3, 3]`. The approach still applies: for each position, multiply all the numbers except the one at that position, and get the correct result even when there are zeros.

If division was allowed, the problem would be straightforward: compute the total product of all elements, then for each element divide the total by the element at that index, resulting in the desired output. Taking our previous example, the product of all elements in `[1, 2, 3, 4]` is 24; dividing 24 by each element gives the expected outputs. However, since division is not allowed, we need a different approach.

We solve this problem using the concepts of "prefix products" and "suffix products." The idea is to compute for each index the product of all numbers to the left (prefix product) and the product of all numbers to the right (suffix product), then multiply these together to get the result for that index.

First, we'll create a prefix product array. The prefix of the first element (1) is just 1, since there is nothing to the left. Then for the second element (2), the prefix product is just the value of the first element, which is 1. For the third element (3), the prefix product is `1 * 2 = 2`. For the fourth element (4), it's `1 * 2 * 3 = 6`. So, the prefix product array is `[1, 1, 2, 6]`.

Now let's build the suffix product array, starting from the right. For the last element (4), the suffix product is 1 (since there is nothing to the right). Next, for the third element (3), the suffix product is just 4. For the second element (2), it's `3 * 4 = 12`. For the first element (1), it's `2 * 3 * 4 = 24`. Thus, the suffix product array is `[24, 12, 4, 1]`.

Once we have both prefix and suffix product arrays, the product for each index `i` (excluding `nums[i]` itself) is simply `prefix[i] * suffix[i]`. This way, for the example `[1, 2, 3, 4]`, we multiply the corresponding elements to get the final answer: `[24, 12, 8, 6]`.

Creating three arrays (prefix, suffix, and answer) results in O(3n) time and space complexity, which simplifies to O(n). This respects the linear-time constraint and avoids using division.

However, we can optimize the space further. Instead of keeping both prefix and suffix arrays, we can use just one array (for the result) plus one variable to track the running suffix product. Here’s how:

- First, fill the result array with the prefix products: Iterate from left to right, for each index i, store the product of all elements to the left of i.
- Then, traverse from right to left, keeping a variable (call it `suffix_product`) initially set to 1. For each index, multiply the current value in the result array (which is the prefix product for that index) by `suffix_product`, and then update `suffix_product` by multiplying it by `nums[i]`.

Using this two-pass approach, we achieve O(n) time and O(1) extra space (excluding the answer array). This is the optimal solution for this problem.

In summary, the key is to understand how to use prefix and suffix products to solve the problem efficiently and without division. First, calculate the prefix product for each element in the answer array. Then, by iterating from right to left, maintain a running suffix product and multiply it with the corresponding value in the answer array to complete the calculation. This technique captures both the required efficiency and the algorithmic insight for interview success.