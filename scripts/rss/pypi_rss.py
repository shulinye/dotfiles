#/usr/bin/python3

import feedparser
import itertools
import re
import sys

FEED = "https://pypi.python.org/pypi?%3Aaction=rss"

re_title = re.compile('([\w.-]+)\s+([\d.]+)')
def pypi(rss, package=None):
    d = feedparser.parse(rss)
    for i in d.entries:
        m = re_title.match(i['title'])
        if m:
            if package:
                if m.groups()[0] in package:
                    print("\nNew version of %s: %s" % m.groups())
                    print("----\n%s" % i['summary'])
            else:
                print("\n%s: %s" % m.groups())
                print("----\n%s" % i['summary'])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('packages', nargs='*')
    args = parser.parse_args()
    if sys.stdin.isatty():
        stdin = []
    else:
        stdin = [i.strip() for i in itertools.takewhile(lambda x: x.strip(), sys.stdin)]
    pypi(FEED, package = set(args.packages).union(stdin))
