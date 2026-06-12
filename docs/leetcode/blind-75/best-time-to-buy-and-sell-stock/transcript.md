# Best Time to Buy and Sell Stock

In this problem, we are given an array of integers, `prices`, where each element represents the price of a stock on a specific day. The goal is to maximize your profit by choosing a single day to buy one stock and a different day in the future to sell that stock.

You can only make one transaction (buy once and sell once), and you must buy before you sell. For example, given prices = [7, 1, 5, 3, 6, 4], the best strategy is to buy at the price of 1 (on day 2), and sell at the price of 6 (on day 5), for a maximum profit of 6 - 1 = 5.

For example, if we are given the array `[7, 1, 5, 3, 6, 4]`, the maximum profit is `5` (buy at 1, sell at 6).

If the prices are always decreasing (e.g., `[7, 6, 4, 3, 1]`), it is impossible to make a profit—since you cannot sell after buying at a lower price. In this case, we return `0` because making no transaction is optimal.

**You can make at most one transaction:** buy one day, sell on a later day, or make no transaction at all if there's no opportunity to profit.

Your task is to determine the maximum profit that can be achieved with these constraints.

## Problem Restatement

For this area, we are making zero transactions, and for this area, we are making one transaction. This is our problem statement.

## Naive Approach: Two Nested Loops

Now let's talk about how to solve this problem. We can solve this problem by running two nested for loops.

## Walkthrough Example

This is the price of stock at first day. In order to maximize the profit, if we buy here, we have to find out the maximum price on the right, which is six. If we buy here, if we sell here, what we'll get, we'll get Minus one. This is negative value, right? Then let's move forward. We wanna buy here, let's find out the maximum price on the right, which is six, so we'll get five, the profit five. Then let's move forward, then we can find out the maximum from right, we'll get the profit one. Let's move forward, we get three, on the right we get six, the maximum on the right six, so we'll get profit at three. Let's move forward, here we get six, on the right we get four, the maximum on the right is four, so we can, so here we can get profit minus, this is negative. From here we're gonna get the maximum. Maximum is 5, so you get return 5.

## Decreasing Order Array

If the array is sorted in decreasing order, we'll get all negative value, so in that case, we'll take maximum of. The initial value of our profit, profit variable is zero, we'll take the maximum of zero minus one, five, one, three, and minus two. For this example, the answer is five, but if the array is sorted in decreasing order, the profit is zero.

## Time and Space Complexity

This is our naive solution. This approach will take time complexity O of n squared and it will take space complexity of one constant. This is not the most efficient solution.

## Linear Time Approach

We can solve this problem in linear time complexity. Let's see how to solve this problem in linear time complexity.

## Efficient Solution Logic

Now let's try to understand the logic of efficient solution Let's assume we raised this element by visiting from the left. We have visited this element, this element, and this element. We raised this element. We can see this price. If we want to sell here, what is the maximum profit we can, what is the maximum amount of profit we can make? We can buy here and we can sell here, right? Then we'll get the profit two, right? We'll get the profit two. We have to capture the minimum value from the, from the left. We have visited this three price already, right? So by visiting this three price, we can capture the minimum value using a variable. Mean price, we can keep track the minimum. So minimum is one on the left. So we can, we can make the profit two. Let's move forward. And here, if we raise this, if we sell here, what is the minimum on the left? We can keep track the minimum price easily using this variable. So if we sell here, what is the profit we'll get? We'll get six minus one, five, right? Let's move forward. Here we have a four. On the lid, the minimum price is one. So if we sell here, we'll get a three. This is the logic, this is the logic to solve this problem efficiently.

## Min Price and Profit Variables

Let's start from the very beginning. Let's create two variable, mean price and Profit. In this profit variable, we'll store the maximum amount of money that we can get. By buying and selling once. This is the initial value. If this array is sorted in decreasing order, the maximum profit would be zero. This is the initial value, and the mean price is the price of stock we have at the first day, which is seven. We're gonna start from the second day from here.

## Walkthrough: Processing Each Day

This is one, right? What is the minimum on the left? If we wanna sell here, what is the profit we'll get? On the minimum we have seven, right? So one minus seven equals to minus six. Max of minus six and zero is zero. Let's move forward.

This is five. Before moving forward, we have to keep track the minimum price, right? Max of minimum of one and seven is one. So if you keep track the minimum price, you have to update this with one. Let's move forward. We get here five. On the left we get the minimum price one, so the profit we will get if we sell here of four, max of zero and four is four. Let's move forward.

This is our, before moving forward we have to check whether this value is less than our min price or not. This value is greater than min price, so let's move forward. Here we see three. On the left, we know the minimum price one. If we sell here, if you buy here, if you buy at minimum price, if we sell here, we'll get the profit two max of two and four is four. Let's check, does this value is less than minimum price? No, so let's move forward.

Here we get six. We get here the value six. The minimum price we know from the left, one, we have in our min price variable. So if we sell here, we'll get a profit five, max of four and five is five. So let's update this value with five. Let's move forward, here we get four. Before that, we have to check whether this value is less than our min price or not. If this value is less than our min price, we have to update min price with our current value. Since this value is greater than min price, so let's move forward. We get here four from the left, we know the min price, we have in our variable. So if we buy here, if we buy here, and if we sell here, we'll get a profit Four minus one equals to three. So max of three and five is five. This is our profit. So we are done. We have processed our array. We find out this profit five. This is our result. So we have to return five, the maximum amount of profit we can generate by buying once and selling once is five, so we have to return five.

## Efficient Solution Complexity

This is the most efficient solution. We are traversing every single element once, so it takes linear time and We are maintaining minimum price and we are keeping our profit using two variable, so it will takes constant space complexity.

## Implementation Preview

Now let's see the implementation of this algorithm. Now let's implement our algorithm. Let's create two There's