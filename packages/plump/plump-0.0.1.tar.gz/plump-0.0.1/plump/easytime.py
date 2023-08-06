import arrow
from time import strftime, localtime



def now():
    return strftime("[%d/%b/%Y %H:%M:%S]", localtime())

def nowA():
    return strftime("%Y%d%m%H%M%S]", localtime())

def last_month():
    return arrow.now().shift(months=-1).format("YYYYMM")

def this_month():
    return arrow.now().format("YYYYMM")

def shift_now(years=0,months=0,days=0):
    return arrow.now().shift(years=years,months=months,days=days).format("YYYYMMDD")

def shift_date(date,years=0,months=0,days=0):
    return arrow.get(date,'YYYYMMDD').shift(years=years,months=months,days=days).format("YYYYMMDD")

def today():
    return arrow.now().format("YYYYMMDD")