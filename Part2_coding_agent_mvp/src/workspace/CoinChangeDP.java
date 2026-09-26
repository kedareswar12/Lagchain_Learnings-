/*
 * Dynamic Programming Problem: Coin Change (Count Ways)
 * ----------------------------------------------------
 * Given a set of distinct positive integer coin denominations and a target amount,
 * determine the number of distinct ways to make up that amount using any number of
 * coins of each denomination. The order of coins does not matter; i.e., [1,2] is
 * the same combination as [2,1].
 *
 * Example:
 *   coins = [1, 2, 5]
 *   amount = 5
 *   The possible combinations are:
 *     1) 5
 *     2) 2 + 2 + 1
 *     3) 2 + 1 + 1 + 1
 *     4) 1 + 1 + 1 + 1 + 1
 *   Hence, the answer is 4.
 *
 * Approach:
 *   This is a classic unbounded knapsack problem and can be solved using dynamic
 *   programming. We maintain an array dp where dp[i] represents the number of ways
 *   to make amount i. The recurrence relation is:
 *       dp[0] = 1 (one way to make amount 0 – using no coins)
 *       For each coin c in coins:
 *           for i from c to amount:
 *               dp[i] += dp[i - c]
 *   The outer loop iterates over coins to ensure combinations are counted
 *   without regard to order.
 */

public class CoinChangeDP {
    /**
     * Returns the number of ways to make up the given amount using the provided coins.
     *
     * @param coins  array of distinct positive coin denominations
     * @param amount target amount (non‑negative)
     * @return number of distinct combinations to form the amount
     */
    public static long countWays(int[] coins, int amount) {
        if (amount < 0) {
            return 0;
        }
        long[] dp = new long[amount + 1];
        dp[0] = 1; // base case
        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                dp[i] += dp[i - coin];
            }
        }
        return dp[amount];
    }

    // Simple demonstration
    public static void main(String[] args) {
        int[] coins = {1, 2, 5};
        int amount = 5;
        long ways = countWays(coins, amount);
        System.out.println("Number of ways to make " + amount + " with coins {1,2,5}: " + ways);
        // Expected output: 4
    }
}
