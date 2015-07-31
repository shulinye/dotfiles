#/usr/bin/python3

from datetime import datetime, timedelta
import os

from zimcommon import Constants

def lastweek(date = datetime.today(),n=7):
    return (os.path.join(Constants.JOURNALDIR.value, (date - timedelta(x)).strftime("%Y/%m/%e.txt")) for x in range(1,n+1))

if __name__ == "__main__":
    mapping = {"lastweek": lastweek}
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_run = subparsers.add_parser('run', help='Run a function?')
    parser_run.add_argument('function', nargs=1)
    args = parser.parse_args()
    run = getattr(args, 'function')[0]
    if run and run in mapping:
        print("\n".join(mapping[run]()))
