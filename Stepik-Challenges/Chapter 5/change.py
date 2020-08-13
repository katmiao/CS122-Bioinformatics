# 5.5 change problem

def DPChange(money, coins):
    minCoins = [float("inf")] * (money + 1)
    minCoins[0] = 0
    for m in range(1, money + 1):
        for i in range(0, len(coins) - 1):
            if m >= coins[i]:
                if minCoins[m - coins[i]] + 1 < minCoins[m]:
                    minCoins[m] = minCoins[m - coins[i]] + 1
    return minCoins[money]

def callDPChange():
    readfile = open('/Users/katmiao/Desktop/CS122/5/input.txt', 'r') 
    money, coins = readfile.read().splitlines()
    readfile.close() 
    money = int(money)
    coins = coins.split(',')
    for c in range(0, len(coins)):
        coins[c] = int(coins[c])

    # money = 40
    # coins = [50, 25, 20, 10, 5, 1]
    print(DPChange(money, coins))

