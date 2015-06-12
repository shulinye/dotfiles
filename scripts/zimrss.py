#!/usr/bin/python3

from datetime import datetime
import feedparser
#Because these scripts require me to look at "secret" rss feeds, I've hidden them in an untracked directly called "sekrit"
import sekrit.rss
import sys
import re

rtm_date = re.compile('<span class=\"rtm_due_value\">(?P<date>[a-zA-Z0-9\s]+)<')

def goodreads(rss, prefix="[ ] "):
    d = feedparser.parse(rss)
    print("Last edited: " + datetime.strftime(datetime.today(), "%A %d %B %Y") + '\n')
    print("%s books" % len(d.entries) + '\n')
    for i in d.entries:
        print(prefix+"//%(title)s// by %(author_name)s - %(link)s" % i)

def rtm(rss, prefix="[ ] ", dateformat="%d %b %y"):
    d = feedparser.parse(rss)
    for i in d.entries:
        date = datetime.strptime(rtm_date.search(i.summary).groups('date')[0], "%a %d %b %y")
        print(prefix+"**DUE "+date.strftime(dateformat)+"**: %(title)s - %(link)s" % i)

if __name__ == "__main__":
    #print(sys.argv)
    if "goodreads" in sys.argv:
        if "to-read" in sys.argv:
            goodreads(sekrit.rss.goodreads["to-read"])
        if "currently-reading" in sys.argv:
            goodreads(sekrit.rss.goodreads["currently-reading"], prefix="* ")
    if "rtm" in sys.argv:
        rtm(sekrit.rss.rtm)
