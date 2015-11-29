import string
import datetime
from datetime import date, timedelta

def query_dates(start, end):
    start_info = string.split(start, "-")
    end_info = string.split(end, "-")

    start_year = int(start_info[0])
    start_month = int(start_info[1])
    start_day = int(start_info[2])

    end_year = int(end_info[0])
    end_month = int(end_info[1])
    end_day = int(end_info[2])

    d1 = date(start_year, start_month, start_day)
    d2 = date(end_year, end_month, end_day)
    
    retarr = [] 
    diff = d2 - d1
    for i in range(diff.days/30):
        pair = list() 
        pair.append((d1 + datetime.timedelta(i*30)).isoformat())
        pair.append((d1 + datetime.timedelta((i+1)*30-1)).isoformat())
        retarr.append(pair)
    
    last_round_start = d1 + datetime.timedelta(diff.days/30*30)
    if last_round_start <= d2:
        pair = list()
        pair.append(last_round_start.isoformat())
        pair.append(d2.isoformat())
        retarr.append(pair)

    return retarr

print query_dates('2015-10-1', '2015-10-30')
