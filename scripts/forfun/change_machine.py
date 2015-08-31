#!/usr/bin/env python3

from collections import OrderedDict
import sys

coins = OrderedDict([
    (100, 'one dollar bill'),
    (25, 'quarter'),
    (10, 'dime'),
    (5, 'nickle'),
    (1, 'penny'),
    ])

def change_machine(change, coins = coins):
    results = [0]*len(coins) #doing this and not appends to make tuple unpacking work
    for index, coin in enumerate(coins):
        results[index], change = divmod(change, coin)
    return results

def main(change):
    print("In order to make change for %d cents:" % change)
    results = change_machine(change, coins)
    for amount, coin in zip(results, coins):
            print("    %d %s(s)" % (amount, coins[coin]))

if __name__ == "__main__":
    main(int(sys.argv[1]))
