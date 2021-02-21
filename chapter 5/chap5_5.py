"""
@BY: Yang LIU
@DATE: 06-10-2020
"""


# Input: An integer money and an array Coins = (coin1, ..., coind).
# Output: The minimum number of coins with denominations Coins that changes money.
def dpchange(money, coins):
    min_num_coins = {}
    min_num_coins[0] = 0
    for m in range(1,money+1):
        min_num_coins[m] = int(money/min(coins))
        for i in range(len(coins)):
            if m >= coins[i]:
                if min_num_coins[m-coins[i]] + 1 < min_num_coins[m]:
                    min_num_coins[m] = min_num_coins[m-coins[i]] + 1
    
    return min_num_coins[money]


if __name__ == "__main__":   

    money = 17904
    coins = [23,7,5,3,1]
    print(dpchange(money, coins))

    # # exercise break
    # coins = [1,4,5]
    # result = ''
    # for money in range(13,23):
    #     result += (str(dpchange(money, coins))+" ")
    # print(result)