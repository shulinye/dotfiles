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
rtm_list = re.compile('<span class=\"rtm_list_value\">(?P<list>[a-zA-Z]+)<')
re_type = re.compile('type=(?P<type>[a-zA-Z0-9\_-]+)')
re_flags = re.compile('^([\w-]+)\=(.*)$', re.MULTILINE|re.UNICODE)

def goodreads(rss, **kwargs):
    arguments = {'prefix': '[ ]'
            }
    arguments.update(kwargs)
    d = feedparser.parse(rss)
    print("Last edited: " + datetime.strftime(datetime.today(), "%A %d %B %Y") + '\n')
    print("%s books" % len(d.entries) + '\n')
    for i in d.entries:
        print(arguments["prefix"]+" //%(title)s// by %(author_name)s - %(link)s" % i)

def rtm(rss, **kwargs):
    arguments = {'prefix': '[ ]',
            'dateformat':"%d %b %y",
            'days':30
            }
    arguments.update(kwargs)
    d = feedparser.parse(rss)
    future = datetime.today() + timedelta(int(arguments['days']))
    for i in d.entries:
        date = datetime.strptime(rtm_date.search(i.summary).groups('date')[0], "%a %d %b %y")
        if date <= future:
            i["location"] = rtm_location.search(i.summary).groups('location')[0]
            listMatch = rtm_list.search(i.summary)
            i["list"] = "(@"+listMatch.groups('list')[0]+")" if listMatch else ''
            print(arguments['prefix']+" **DUE " + date.strftime(arguments['dateformat'])+"**: %(title)s @ %(location)s %(list)s- %(link)s" % i)

if __name__ == "__main__":
    arguments = "\n".join(sys.argv)
    
    flags = {i.groups()[0]: i.groups()[1] for i in re_flags.finditer(arguments)}

    typeMatch = re_type.search(arguments)
    typeOption = functools.reduce(operator.add, [i.split(",") for i in typeMatch.groups('type')], []) if typeMatch else []
    typeOption = [i.lower() for i in typeOption]

    if "goodreads" in sys.argv:
        for i in typeOption:
            goodreads(sekrit.rss.goodreads[i], **flags)
    if "rtm" in sys.argv:
        for i in typeOption:
            rtm(sekrit.rss.rtm[i], **flags)
