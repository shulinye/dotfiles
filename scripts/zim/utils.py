from datetime import datetime, timedelta

def lastweek(date = datetime.today(),n=7):
    return '\n'.join([(date - timedelta(x)).strftime("%Y/%m/%e") for x in range(1,n=1)])
