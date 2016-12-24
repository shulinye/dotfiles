#/usr/bin/python3

from calendar import TextCalendar
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import os

today = datetime.today()

from zimcommon import Constants

def lastweek(date : str = None, n : int = 7):
    if date:
        date = dateparser.parse(date)
    else:
        date = datetime.today()
    return (os.path.join(Constants.JOURNALDIR.value, (date - timedelta(x)).strftime("%Y/%m/%d.txt")) for x in range(1,n+1))

def asciiMonth(year : int = today.year, month : int = today.month):
    return ("''%s''" % i for i in TextCalendar(0).formatmonth(year,month).split('\n'))

if __name__ == "__main__":
    mapping = {"lastweek": lastweek,
               "asciiMonth": asciiMonth}
    import argparse
    import inspect
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for name, func in mapping.items():
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(which=name)
        params = inspect.signature(func).parameters
        for i,j in func.__annotations__.items():
            subparser.add_argument("--" + i, type=j, default=params[i].default)
    args = parser.parse_args()
    val = mapping[args.which](**{k:v for k,v in vars(args).items() if k != "which"})
    if hasattr(val, "__iter__"):
        for i in val:
            print(i)
    else:
        print(val)
