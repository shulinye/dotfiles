#!/usr/bin/python3

from datetime import datetime
import feedparser
import sekrit.rss
import sys

def goodreads(rss, prefix="[ ] "):
    d = feedparser.parse(rss)
    print("Last edited: " + datetime.strftime(datetime.today(), "%A %d %B %Y") + '\n')
    print("%s books" % len(d.entries) + '\n')
    for i in d.entries:
        print(prefix+"//%(title)s// by %(author_name)s" % i)

if __name__ == "__main__":
    #print(sys.argv)
    if "goodreads" in sys.argv:
        if "to-read" in sys.argv:
            goodreads(sekrit.rss.goodreads["to-read"])
