#!/usr/bin/env python

from collections import OrderedDict
from decimal import Decimal, ROUND_HALF_EVEN
import re
import sys

coins = OrderedDict([
    (10000, 'one hundred dollar bill'),
    (5000, 'fifty dollar bill'),
    (2000, 'twenty dollar bill'),
    (1000, 'ten dollar bill'),
    (500, 'five dollar bill'),
    (100, 'one dollar bill'),
    (25, 'quarter'),
    (10, 'dime'),
    (5, 'nickle'),
    (1, 'penny'),
    ])

plural = {i:i+'s' for i in coins.values()}
plural.update({'penny': 'pennies'})

PLACES = 2
m = re.compile('\d*\.?\d*')

def parse_money(money, places = PLACES):
    return Decimal(m.search(money).group()).quantize(Decimal(10)**-places, rounding=ROUND_HALF_EVEN)

def change_machine(change, coins = coins):
    results = [0]*len(coins) #doing this and not appends to make tuple unpacking work
    # bankers rounding, even in python2
    change = int(Decimal(change).quantize(Decimal('1'), rounding=ROUND_HALF_EVEN))
    for index, coin in enumerate(coins):
        results[index], change = divmod(change, coin)
        if change == 0: break
    return results

def main(change, cents_in_dollar=10**PLACES):
    change = parse_money(change)
    print("In order to make change for $%s:" % change)
    results = change_machine(change*cents_in_dollar, coins)
    for amount, coin in zip(results, coins.values()):
        if amount > 0: print("    %d %s" % (amount, coin if amount==1 else plural[coin]))

if __name__ == "__main__":
    for i in sys.argv[1:]:
        main(i)
        print("")
