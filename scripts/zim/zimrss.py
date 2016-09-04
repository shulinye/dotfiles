#!/usr/bin/env python3

from datetime import datetime, timedelta
import feedparser
# Because these scripts require me to look at "secret" rss feeds
# I've hidden them in an untracked directory called "sekrit",
# in a file called "rss.py".
# I've stored the relevant rss feeds in collections.defaultdict
import sekrit.rss
import sys
import re
import operator
import functools
import warnings

rtm_date = re.compile(r'<span class="rtm_due_value">(?P<date>[a-zA-Z0-9\s:]+)<')
rtm_location = re.compile(r'<span class="rtm_location_value">(?P<location>[a-zA-Z0-9\s]+)<')
rtm_list = re.compile(r'<span class="rtm_list_value">(?P<list>[a-zA-Z]+)<')

def goodreads(rss, prefix : str = '[ ]'):
    d = feedparser.parse(rss)
    print("Last edited: " + datetime.strftime(datetime.today(), "%A %d %B %Y") + '\n')
    print("%s books" % len(d.entries) + '\n')
    for i in d.entries:
        print(prefix + " //%(title)s// by %(author_name)s - %(link)s" % i)


def rtm(rss, prefix : str = '[ ]', dateformat : str = '%d %b %y', days : int = 30):
    d = feedparser.parse(rss)
    future = datetime.today() + timedelta(days)
    for i in d.entries:
        date_match = rtm_date.search(i.summary)
        if date_match:
            date_string = date_match.groups('date')[0].strip()
            if 'never' in date_string:
                continue
            if ' at ' in date_string:
                date_string, time = date_string.split(' at ')
                time = ' ' + time
            else:
                time = ''
            try:
                date = datetime.strptime(date_string.strip(), "%a %d %b %y")
            except ValueError:
                warnings.warn("Bad date string: " + i.summary, RuntimeWarning)
            else:
                if date <= future:
                    i["location"] = rtm_location.search(i.summary).groups('location')[0]
                    listMatch = rtm_list.search(i.summary)
                    i["list"] = " ( @"+listMatch.groups('list')[0]+" )" if listMatch else ''
                    print(("{0} **DUE {1}{2}**: %(title)s @ %(location)s%(list)s - %(link)s" \
                            .format(prefix, date.strftime(dateformat), time)) % i)
        else:
            warnings.warn("dateless: " + i.summary, RuntimeWarning)
            

if __name__ == "__main__":
    import argparse
    import inspect
    mapping = {'goodreads': goodreads,
               'rtm': rtm}
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for name, func in mapping.items():
        subparse = subparsers.add_parser(name)
        subparse.set_defaults(rss=name)
        subparse.add_argument("subtype", nargs=1, choices=getattr(sekrit.rss, name).keys())
        params = inspect.signature(func).parameters
        for i,j in func.__annotations__.items():
            subparse.add_argument("--" + i, type=j, default=params[i].default)
    args = parser.parse_args()
    rss = getattr(sekrit.rss, args.rss)
    subtype = rss[args.subtype[0]]
    kwargs = {k:v for k,v in vars(args).items() if k not in ('rss', 'subtype')}
    mapping[args.rss](subtype,**kwargs)
