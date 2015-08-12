#!/usr/bin/python3

from os import path
import requests
from urllib.parse import quote

BASEPATH = path.dirname(path.realpath(__file__))
FLAG_FILE = path.join(BASEPATH, "flags.txt")
# https://code.google.com/p/yahoo-finance-managed/wiki/enumQuoteProperty
# in a text file

FLAGS = {}

with open(FLAG_FILE) as f:
    next(f)
    for i in f:
        name, *des, flag = i.split()
        FLAGS[flag] = " ".join(des)

def try_convert(x, _type=float):
    try:
        return _type(x)
    except ValueError:
        return x

def get_stock_values(*stocks, flags=['n','s','l1','o','p']):
    URL_FORMAT = "http://download.finance.yahoo.com/d/quotes.csv?s={stocks}&f={flags}&e=.csv"
    URL = URL_FORMAT.format(stocks=",".join(map(quote,stocks)), flags=''.join(flags))
    val = requests.get(URL)
    for i in val.content.decode('utf-8').split('\n'):
        if i != '':
            res = map(lambda x: try_convert(x.replace('"', '')), i.split(','))
            yield dict(zip(map(FLAGS.__getitem__, flags), res))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('stocks', nargs='+')
    for f, name in FLAGS.items():
        parser.add_argument('--' + f, help=name, action='store_true')
    args = parser.parse_args()
    choices = list(filter(lambda x: getattr(args,x), FLAGS)) or ['l1','o','p']
    choices += ['n','s']
    ret = get_stock_values(*args.stocks, flags = choices)
    for i in ret:
        print(i)
