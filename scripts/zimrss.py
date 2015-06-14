#!/usr/bin/python3

from datetime import datetime, timedelta
import feedparser
#Because these scripts require me to look at "secret" rss feeds, I've hidden them in an untracked directory called "sekrit"
#In a file called "rss.py", I've stored the relevant rss feeds in collections.defaultdict
import sekrit.rss
import sys
import re
import operator
import functools

rtm_date = re.compile('<span class=\"rtm_due_value\">(?P<date>[a-zA-Z0-9\s]+)<')
rtm_location = re.compile('<span class=\"rtm_location_value\">(?P<location>[a-zA-Z0-9\s]+)<')
re_prefix = re.compile('prefix=(?P<prefix>[^\s]+)')
re_type = re.compile('type=(?P<type>[a-zA-Z0-9\_-]+)')
re_days = re.compile('days=(?P<days>[0-9]+)')

def goodreads(rss, prefix='[ ]'):
    d = feedparser.parse(rss)
    print("Last edited: " + datetime.strftime(datetime.today(), "%A %d %B %Y") + '\n')
    print("%s books" % len(d.entries) + '\n')
    for i in d.entries:
        print(prefix+" //%(title)s// by %(author_name)s - %(link)s" % i)

def rtm(rss, prefix='[ ]', dateformat="%d %b %y", days=30):
    d = feedparser.parse(rss)
    future = datetime.today() + timedelta(days)
    for i in d.entries:
        date = datetime.strptime(rtm_date.search(i.summary).groups('date')[0], "%a %d %b %y")
        i["location"] = rtm_location.search(i.summary).groups('location')[0]
        if date <= future:
            print(prefix+" **DUE " + date.strftime(dateformat)+"**: %(title)s @ %(location)s- %(link)s" % i)

if __name__ == "__main__":
    arguments = " ".join(sys.argv)

    prefixMatch = re_prefix.search(arguments)
    prefix = prefixMatch.groups('prefix')[0] if prefixMatch else '[ ]'

    typeMatch = re_type.search(arguments)
    typeOption = functools.reduce(operator.add, [i.split(",") for i in typeMatch.groups('type')], []) if typeMatch else []

    daysMatch = re_days.search(arguments)
    days = int(daysMatch.groups('days')[0]) if daysMatch else 30

    if "goodreads" in sys.argv:
        for i in typeOption:
            goodreads(sekrit.rss.goodreads[i], prefix=prefix)
    if "rtm" in sys.argv:
        for i in typeOption:
            rtm(sekrit.rss.rtm[i], prefix=prefix, days=days)
